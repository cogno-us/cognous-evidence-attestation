"""Three development spot checks of the Verifier-result attestation profile (not qualification)."""
import copy
import hashlib
from pathlib import Path

import pytest

from api import attestations
from main import app
from models.verification import AttestationEnvelope
from profiles.verifier_result import (
    AUDIENCE, NOT_VERIFIED, STATEMENT_TYPE, build_unsigned_statement, verify_verifier_result,
)
from tests.verifier_result_signing import ISSUER, KEY_ID, ephemeral_signer, sign
from utils.trust import TrustRegistry

NOW = 1800000000
VERIFIER_REVISION = "2ffe37c5ea1255e9699972980f0cb33c06a080e2"
FIXTURES = Path(__file__).parent / "fixtures" / "verifier-result"


@pytest.fixture
def dev(client_factory):
    key, registry_data = ephemeral_signer(NOW)
    return key, registry_data, client_factory(registry_data)


@pytest.fixture
def client_factory(session_factory):
    from fastapi.testclient import TestClient
    from api import governance, identity, integration

    clients = []

    def make(registry_data):
        def get_db():
            with session_factory() as db:
                yield db
        for module in (attestations, identity, governance, integration):
            app.dependency_overrides[module.get_db] = get_db
        app.dependency_overrides[attestations.get_trust] = lambda: TrustRegistry.model_validate(copy.deepcopy(registry_data))
        app.dependency_overrides[attestations.get_now] = lambda: NOW
        tc = TestClient(app)
        clients.append(tc)
        return tc

    yield make
    app.dependency_overrides.clear()


def _statement(raw: bytes):
    return build_unsigned_statement(raw, verifier_revision=VERIFIER_REVISION, issuer=ISSUER, key_id=KEY_ID, now=NOW)


def test_1_complete_report_signed_verified_admitted_and_read_back(dev):
    key, registry_data, client = dev
    raw = (FIXTURES / "complete.report.json").read_bytes()
    statement = _statement(raw)
    envelope = sign(key, statement)
    registry = TrustRegistry.model_validate(registry_data)
    result = verify_verifier_result(raw, AttestationEnvelope.model_validate(envelope), registry, NOW)
    assert result.accepted and result.assurance == "issuer_signature_only" and result.native_outcome == "verified"
    assert result.report_overall == "abstain"  # the Verifier conclusion is unchanged, not promoted
    assert result.verifier_revision_asserted == VERIFIER_REVISION
    assert statement.statement_type == STATEMENT_TYPE and statement.audience == AUDIENCE
    assert statement.expires_at - statement.not_before == 900
    assert statement.content_digest == "sha256:" + hashlib.sha256(raw).hexdigest()
    assert statement.content_digest != result.statement_digest  # report digest vs native statement digest
    assert VERIFIER_REVISION in statement.attestation_id  # revision bound inside signed content

    posted = client.post("/attest", json=envelope)
    assert posted.status_code == 201, posted.text
    assert posted.json()["verification"]["assurance"] == "issuer_signature_only"
    read = client.get(f"/attestations/{result.statement_digest}")
    assert read.status_code == 200
    record = read.json()
    assert record["attestation"] == envelope  # the readback is the admitted statement
    assert record["verification"]["outcome"] == "verified"
    assert hashlib.sha256(raw).hexdigest() == record["attestation"]["statement"]["content_digest"][len("sha256:"):]
    again = verify_verifier_result(raw, AttestationEnvelope.model_validate(record["attestation"]), registry, NOW)
    assert again.accepted and again.report_overall == "abstain"


def test_2_altered_signed_content_is_refused_natively(dev):
    key, registry_data, client = dev
    raw = (FIXTURES / "complete.report.json").read_bytes()
    envelope = sign(key, _statement(raw))
    envelope["statement"]["content_digest"] = "sha256:" + hashlib.sha256(b"another report").hexdigest()
    result = verify_verifier_result(raw, AttestationEnvelope.model_validate(envelope), TrustRegistry.model_validate(registry_data), NOW)
    assert not result.accepted and result.reason == "invalid_signature"
    assert result.native_outcome == "rejected" and result.assurance == "none"
    posted = client.post("/attest", json=envelope)
    assert posted.status_code == 422 and posted.json()["detail"]["reason"] == "invalid_signature"


def test_3_partial_report_keeps_abstain_and_absent_execution_evidence(dev):
    key, registry_data, client = dev
    raw = (FIXTURES / "partial.report.json").read_bytes()
    envelope = sign(key, _statement(raw))
    result = verify_verifier_result(raw, AttestationEnvelope.model_validate(envelope), TrustRegistry.model_validate(registry_data), NOW)
    assert result.accepted and result.assurance == "issuer_signature_only"  # a signature fact only
    assert result.report_overall == "abstain"
    assert set(result.report_execution_absent) == {
        "execution_envelope", "execution_result", "destination_attempt", "destination_effect"}
    assert any(c.startswith("independent_execution_verification") for c in result.report_unsupported_claims)
    assert "execution_occurred" in result.not_verified and set(NOT_VERIFIED) <= set(result.not_verified)
    assert client.post("/attest", json=envelope).status_code == 201
