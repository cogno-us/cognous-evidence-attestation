"""Optional, development-only profile: attest the exact bytes of a Verifier result.

DEVELOPMENT ONLY / NON-AUTHORIZING. This module composes the accepted BitRep v1 verifier
without changing it. It builds an UNSIGNED `bitrep-attestation/1` statement over the exact bytes of an
`evidence-pack-verification/0.1.0-dev` report, and it checks a separately signed envelope against the
report bytes and an explicitly supplied trust snapshot.

It never signs, never loads or creates keys, never enrolls an issuer and never stores anything. Signing
for development lives only in the test helper. A verified result means the enrolled key signed those
statement bytes (`issuer_signature_only`). It does not show that the report is correct, that the
Evidence Pack was genuine, that anything executed, that the Verifier revision is authentic, or that the
signer holds any authority. The Verifier verdict is bound only through the content digest, because the
v1 statement has no field for it; the verdict is re-read from the report bytes and never promoted.
"""
import hashlib
import re
from typing import Annotated, Literal

from pydantic import Field, ValidationError

from models.verification import AttestationEnvelope, Epoch, SignedStatement, StrictModel
from utils.trust import TrustRegistry, strict_json
from utils.verification import PROTOCOL_VERSION, statement_digest, verify_attestation

PROFILE_ID = "cognous-verifier-result-attestation/1"
STATEMENT_TYPE = "cognous.verifier-result.dev/1"
AUDIENCE = "cognous-ocs-vnext-s4-dev"
WINDOW_SECONDS = 900
REPORT_CONTRACT = "evidence-pack-verification"
REPORT_CONTRACT_VERSION = "0.1.0-dev"
ID_PREFIX = "cognous-vr-dev/1/rev-"
_ID = re.compile(r"^cognous-vr-dev/1/rev-([0-9a-f]{40})/([0-9a-f]{64})$")
_DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
_REVISION = re.compile(r"^[0-9a-f]{40}$")
OVERALLS = ("reject", "abstain", "unsupported")  # the Verifier never emits accept for a pack

NOT_VERIFIED = (
    "report_correctness",
    "evidence_pack_genuineness",
    "execution_occurred",
    "verifier_revision_authenticity",
    "signer_institutional_authority",
    "independent_custody",
    "independent_qualification",
)


class ProfileRefusal(ValueError):
    """The report bytes or statement do not fit this profile."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class ReportFacts(StrictModel):
    """What the report states about itself. Read from the bytes; not authenticated."""

    subject_digest: Annotated[str, Field(pattern=r"^sha256:[0-9a-f]{64}$")]
    overall: Literal["reject", "abstain", "unsupported"]
    unsupported_claims: tuple[str, ...]
    execution_absent: tuple[str, ...]


class VerifierResultVerification(StrictModel):
    """Local profile result. `accepted` means signature and bindings only, never Verifier acceptance."""

    result_version: Literal["cognous-verifier-result-verification/1-dev"] = (
        "cognous-verifier-result-verification/1-dev"
    )
    profile: Literal["cognous-verifier-result-attestation/1"] = PROFILE_ID
    accepted: bool
    reason: str
    assurance: Literal["issuer_signature_only", "none"]
    native_outcome: Literal["verified", "rejected"]
    statement_digest: str
    content_digest: str
    verifier_revision_asserted: str | None = None
    report_overall: str | None = None
    report_unsupported_claims: tuple[str, ...] = ()
    report_execution_absent: tuple[str, ...] = ()
    not_verified: tuple[str, ...] = NOT_VERIFIED
    evaluated_at: Epoch


def report_digest(raw: bytes) -> str:
    """SHA-256 of the exact report bytes. Nothing is parsed or normalized first."""
    if not isinstance(raw, bytes):
        raise ProfileRefusal("report_not_bytes")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def parse_report(raw: bytes) -> ReportFacts:
    """Read the facts this profile needs, or refuse. The report is not treated as authenticated."""
    if not isinstance(raw, bytes):
        raise ProfileRefusal("report_not_bytes")
    try:
        doc = strict_json(raw)
    except (ValueError, RecursionError) as exc:
        raise ProfileRefusal("report_not_strict_json") from exc
    if not isinstance(doc, dict):
        raise ProfileRefusal("report_not_object")
    if doc.get("contract") != REPORT_CONTRACT or doc.get("contract_version") != REPORT_CONTRACT_VERSION:
        raise ProfileRefusal("report_contract_unsupported")
    if doc.get("development_only") is not True:
        raise ProfileRefusal("report_not_development_only")
    subject = doc.get("subject")
    digest = subject.get("digest") if isinstance(subject, dict) else None
    if not isinstance(digest, str) or not _DIGEST.fullmatch(digest):
        raise ProfileRefusal("report_subject_digest_invalid")
    overall = doc.get("overall")
    if overall not in OVERALLS:
        raise ProfileRefusal("report_overall_unsupported")
    claims = doc.get("unsupported_claims")
    if not isinstance(claims, list) or not all(isinstance(c, str) for c in claims):
        raise ProfileRefusal("report_unsupported_claims_invalid")
    evidence = doc.get("execution_evidence")
    if overall != "unsupported" and not (isinstance(evidence, dict) and "absent" in evidence):
        # a supported-profile report states which execution evidence is absent; omission is not 'none absent'
        raise ProfileRefusal("report_execution_evidence_missing")
    absent = evidence.get("absent", []) if isinstance(evidence, dict) else []
    if not isinstance(absent, list) or not all(isinstance(a, str) for a in absent):
        raise ProfileRefusal("report_execution_evidence_invalid")
    try:
        return ReportFacts(
            subject_digest=digest, overall=overall,
            unsupported_claims=tuple(claims), execution_absent=tuple(absent),
        )
    except ValidationError as exc:
        raise ProfileRefusal("report_facts_invalid") from exc


def make_attestation_id(verifier_revision: str, content_digest: str) -> str:
    """Versioned profile convention that places the asserted Verifier revision in signed content."""
    if not _REVISION.fullmatch(verifier_revision):
        raise ProfileRefusal("verifier_revision_invalid")
    if not _DIGEST.fullmatch(content_digest):
        raise ProfileRefusal("content_digest_invalid")
    return f"{ID_PREFIX}{verifier_revision}/{content_digest[len('sha256:'):]}"


def build_unsigned_statement(
    report: bytes, *, verifier_revision: str, issuer: str, key_id: str, now: int
) -> SignedStatement:
    """The unsigned statement for these exact report bytes. The caller signs it elsewhere."""
    facts = parse_report(report)
    content = report_digest(report)
    attestation_id = make_attestation_id(verifier_revision, content)
    try:
        return SignedStatement(
            protocol_version=PROTOCOL_VERSION, algorithm="Ed25519",
            attestation_id=attestation_id,
            issuer=issuer, key_id=key_id, subject=facts.subject_digest,
            statement_type=STATEMENT_TYPE, audience=AUDIENCE, content_digest=content,
            issued_at=now, not_before=now, expires_at=now + WINDOW_SECONDS,
        )
    except ValidationError as exc:
        raise ProfileRefusal("statement_fields_invalid") from exc


def _binding_refusal(report: bytes, statement: SignedStatement) -> tuple[str, str | None]:
    """First profile binding that fails, or ('ok', asserted revision)."""
    match = _ID.fullmatch(statement.attestation_id)
    if statement.statement_type != STATEMENT_TYPE:
        return "statement_type_mismatch", None
    if statement.audience != AUDIENCE:
        return "profile_audience_mismatch", None
    if match is None:
        return "attestation_id_convention_mismatch", None
    content = report_digest(report)
    if statement.content_digest != content:
        return "content_digest_mismatch", None
    if match.group(2) != content[len("sha256:"):]:
        return "attestation_id_digest_mismatch", None
    if statement.expires_at - statement.not_before > WINDOW_SECONDS:
        return "validity_window_too_long", None
    try:
        facts = parse_report(report)
    except ProfileRefusal as exc:
        return exc.reason, None
    if statement.subject != facts.subject_digest:
        return "subject_mismatch", None
    return "ok", match.group(1)


def verify_verifier_result(
    report: bytes, envelope: AttestationEnvelope, registry: TrustRegistry, now: int
) -> VerifierResultVerification:
    """Native signature/trust verification first, then the profile bindings to the report bytes.

    `TrustUnavailable` from the native verifier is not caught: no usable trust means no result.
    """
    statement = envelope.statement
    native = verify_attestation(envelope, registry, now)
    reason, revision = (native.reason, None) if native.outcome != "verified" else _binding_refusal(report, statement)
    accepted = native.outcome == "verified" and reason == "ok"
    try:
        facts: ReportFacts | None = parse_report(report)
    except ProfileRefusal:
        facts = None
    return VerifierResultVerification(
        accepted=accepted, reason=reason,
        assurance="issuer_signature_only" if accepted else "none",
        native_outcome=native.outcome,
        statement_digest=statement_digest(statement),
        content_digest=statement.content_digest,
        verifier_revision_asserted=revision if accepted else None,
        report_overall=facts.overall if facts else None,
        report_unsupported_claims=facts.unsupported_claims if facts else (),
        report_execution_absent=facts.execution_absent if facts else (),
        evaluated_at=now,
    )
