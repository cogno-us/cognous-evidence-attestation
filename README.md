<!-- cognous-banner:start -->
```text
──────────────────────────────────────────────────
   __________  _______   ______  __  _______
  / ____/ __ \/ ____/ | / / __ \/ / / / ___/
 / /   / / / / / __/  |/ / / / / / / /\__ \
/ /___/ /_/ / /_/ / /|  / /_/ / /_/ /___/ /
\____/\____/\____/_/ |_/\____/\____//____/
           COGNOUS EVIDENCE ATTESTATION
       g o v e r n e d   b y   d e s i g n
  github.com/cogno-us/cognous-open-control-stack
──────────────────────────────────────────────────
```
<!-- cognous-banner:end -->

# Cognous Evidence Attestation

**Verify issuer signatures under explicit trust assumptions.**

**Status:** group 01 · Knowledge & Provenance; lock status **selected** (interface: verification contract v1, recorded in [component-lock.json](https://github.com/cogno-us/cognous-open-control-stack/blob/main/component-lock.json)); the authority-digest custody profile is **proposed** and optional; contract drafts stay `0.1.0-draft`. A successful result means `issuer_signature_only`. Nothing here is a release; operational trust remains [HOLD under #30](https://github.com/cogno-us/cognous-stack-orchestrator/issues/30). The verification contract document keeps its original proposal-stage header ("proposed cross-component contract pending Governor review"); the lock, not that header, records what is selected.

## What it is

A binary-attestation protocol and reference verifier (BitRep). The selected v1 interface checks an Ed25519 signature over a strict statement against an operator-configured issuer-key trust snapshot and an evaluation time. A successful result means `issuer_signature_only` under those conditions. It does not establish factual truth, that the signer is who the name says, content availability or institutional authority, and it is non-authorizing.

**Who it is for.** An evidence consumer who needs to know who signed a statement, which content it commits to and whether the key and statement are admissible now. Engineers can inspect the reference contracts and examples; architecture, security and governance reviewers can examine the boundary and the evidence it leaves. Evaluate this component for its named responsibility rather than as a complete governance platform.

**What it does not do.** No reputation score, real zero-knowledge proof, external-platform identity verification, blockchain inclusion verification, signed portable result receipt or caller-selected historical verification is established by v1. Issuer enrollment, secure time, snapshot distribution and anti-rollback, and production transport authentication remain deployment work. A valid signature, chain inclusion, message receipt, reasoning instruction or evidence-package digest does not authorize execution. See [what it does not do](#what-it-does-not-do-known-limits).

**Synthetic example.** A publisher and an independent witness may commit the digest of a synthetic policy version. A mismatch or a revoked key fails verification. Even successful custody verification does not establish that the institution adopted that policy or authorized an effect.

## Where it fits

<a id="cognous-stack-components"></a>

<!-- stack-map:start -->
<!-- Canonical block: identical text in every component README. Source: docs/stack-map.md in the hub. Refresh at the pin round. -->
The Open Control Stack groups its repositories by responsibility. The groups are a navigation map, not an execution sequence and not a requirement to install every component. The hub [component lock](https://github.com/cogno-us/cognous-open-control-stack/blob/main/component-lock.json) is the only source of selected revisions; [release status](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/release-status.md) states their evidence and limits. Last checked against `component-lock.json` at hub commit `dcc9bd7533ef`.

| Group | Members |
| --- | --- |
| **01 Knowledge & Provenance** | [Evidence Registry (The Index)](https://github.com/cogno-us/cognous-evidence-registry) · [Evidence Attestation (BitRep)](https://github.com/cogno-us/cognous-evidence-attestation) |
| **02 Institutional Governance** | [Institutional Governance (Alvorada)](https://github.com/cogno-us/cognous-institutional-governance) |
| **03 Declaration & Policy Control** | [Action Manifest](https://github.com/cogno-us/cognous-action-manifest) · [Control Plane](https://github.com/cogno-us/cognous-control-plane) |
| **04 Constrained Execution** | [Execution Runtime](https://github.com/cogno-us/cognous-execution-runtime) |
| **05 Replay & Evidence** | [Replay Bundle](https://github.com/cogno-us/cognous-replay-bundle) · [Governance Evidence Pack](https://github.com/cogno-us/cognous-governance-evidence-pack) · [ODES](https://github.com/cogno-us/open-decision-evidence-standard) |
| **Cross-cutting exchange** | [Governed Exchange (GAX/IMX)](https://github.com/cogno-us/cognous-governed-exchange) |
| **Tooling and qualification** (side group) | [Ergonomics (`cognous-ocs`)](https://github.com/cogno-us/cognous-open-control-stack-ergonomics) · [Verifier](https://github.com/cogno-us/cognous-open-control-stack-verifier) · [Orchestrator](https://github.com/cogno-us/cognous-stack-orchestrator) · [Qualification](https://github.com/cogno-us/cognous-stack-qualification) |

Status labels used in this README: **merged** (reviewed and merged in the owning repository; not by itself selected), **selected** (pinned in the hub lock), **known limit** (a limitation that is stated and kept visible) and **proposed** (draft or planned work, not a supported interface). Full map, names and commands: [stack map](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/stack-map.md), [naming](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/naming.md), [profiles and tools](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/profiles-and-tools.md). A signature, registry entry, message receipt or evidence summary does not grant execution authority.
<!-- stack-map:end -->

This component sits in group 01, beside [Evidence Registry](https://github.com/cogno-us/cognous-evidence-registry), which supplies the expected subject, audience and content binding and records attestations off-chain. [Institutional Governance](https://github.com/cogno-us/cognous-institutional-governance) names the custody profile below as a consumer need. The consumer still compares the digest with the exact bytes it uses and decides how much weight to give the assertion; two signed assertions about the same bytes are not automatically independent corroboration. Revision-specific qualification commentary is in the [central test hub](https://github.com/cogno-us/cognous-stack-qualification/blob/main/results/readme-commentary/index.md); for the full selected integration use the hub [quickstart](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/quickstart.md), whose runner supplies exact producer checkouts and test wiring.

## Quick start

Prerequisites: Linux, Python 3.11 or newer (CI uses 3.11; 3.13 was also run), an activated virtual environment and network access for the install. Install only into that environment. Everything after the install runs locally. From a fresh checkout:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q tests
```

Expected: `95 passed` in about ten seconds, with about twenty deprecation warnings from third-party libraries (they concern the HTTP test client and `datetime.utcnow()` in the legacy governance code). The tests use synthetic fixtures and ephemeral keys.

Then verify the shipped synthetic fixture. The script uses the public key and signature in `tests/fixtures/verification-v1.json` (a public synthetic test key, never deploy it), checks it, then repeats the check after changing one signed field and again at a later time. Save it as `verify_demo.py` in the repository root and run `PYTHONPATH=. python verify_demo.py`:

```python
import json
from models.verification import AttestationEnvelope
from utils.trust import TrustRegistry
from utils.verification import verify_attestation

fixture = json.load(open("tests/fixtures/verification-v1.json"))
trust = TrustRegistry.model_validate(fixture["trust"])
now = fixture["evaluated_at"]

good = verify_attestation(AttestationEnvelope.model_validate(fixture["attestation"]), trust, now)
print("signed statement :", good.outcome, good.reason, good.assurance)

fixture["attestation"]["statement"]["subject"] = "claim:other"
bad = verify_attestation(AttestationEnvelope.model_validate(fixture["attestation"]), trust, now)
print("subject changed  :", bad.outcome, bad.reason)

late = verify_attestation(AttestationEnvelope.model_validate(json.load(open("tests/fixtures/verification-v1.json"))["attestation"]), trust, now + 500)
print("evaluated later  :", late.outcome, late.reason)
```

Expected output:

```text
signed statement : verified ok issuer_signature_only
subject changed  : rejected invalid_signature
evaluated later  : rejected attestation_expired
```

The first line is the result this component produces, and its meaning is limited: the configured key signed exactly those bytes at the evaluation time. It is not evidence that the claim about `claim:42` is true, that the issuer is who it says, or that anything is authorized. The other two lines are negative facts kept on purpose: any change to a signed field, or an evaluation time after expiry, is refused.

A service deployment additionally needs an operator-controlled `BITREP_TRUST_REGISTRY` (a local trust snapshot file), trusted time and appropriate access controls. Without a usable snapshot the verification and admission endpoints answer 503. Test keys and copied verification JSON are not production credentials. Setup commands: [developer setup](DEVELOPER_SETUP.md).

## What ships

| Item | Where | Label | Page |
| --- | --- | --- | --- |
| v1 verification (signed statement, trust snapshot, `issuer_signature_only`) | `utils/verification.py`, `utils/trust.py`, `models/verification.py` | selected (verification contract v1) | [verification contract](docs/VERIFICATION_CONTRACT_V1.md) |
| v1 HTTP interface: `POST /verify` (check, store nothing), `POST /attest` (check, then admit), `GET /attestations/{digest}` | `api/attestations.py`, `main.py` | selected | [verification contract](docs/VERIFICATION_CONTRACT_V1.md) |
| Accepted-record storage, kept separate from legacy rows | `models/attestation.py`, `db/schema.sql` | selected | [validation record](docs/VALIDATION_V1.md) |
| Four JSON schemas: attestation, trust snapshot, verification result, custody claim | [attestation](docs/attestation-v1.schema.json), [trust](docs/trust-v1.schema.json), [verification](docs/verification-v1.schema.json), [authority digest custody](docs/authority-digest-custody-v1.schema.json) | contract draft | [verification contract](docs/VERIFICATION_CONTRACT_V1.md) |
| Authority-digest custody profile: publisher claim plus witness commitment, result `non_authorizing_digest_custody` | `profiles/authority_digest_custody.py` | proposed, optional | [custody profile](docs/AUTHORITY_DIGEST_CUSTODY_PROFILE_V1.md) |
| Decision record for the verification boundary | none | selected | [ADR 001](docs/ADR-001-verification-boundary.md) |
| Synthetic fixtures and tests (95 tests) | `tests/` | selected | [validation record](docs/VALIDATION_V1.md) |
| Legacy prototype API: `/identity/*`, `/user/*`, `/governance/*`, `/integration/*` | `api/identity.py`, `api/users.py`, `api/governance.py`, `api/integration.py` | legacy; known limit: identities are names and no request is signature-bound | [threat model](THREAT_MODEL.md) |
| Legacy privacy routes `/privacy/*` | `api/privacy.py` | legacy; answer 501 `demonstration_only`, assurance `none` | [verification contract](docs/VERIFICATION_CONTRACT_V1.md) |
| Legacy RSA and demonstration zero-knowledge helpers | `utils/crypto.py`, `utils/zkproof.py` | legacy; not accepted by v1 | [security policy](SECURITY.md) |
| Business and one-page overviews | `collateral/` | non-technical | [business overview](collateral/business-collateral.md), [one-page overview](collateral/one-page-overview.md) |

The custody profile's verifier (`verify_authority_digest_custody`) fails closed in a fixed order. Two checks are worth knowing: the claim carries an effective interval and the supplied evaluation time must fall inside it, otherwise the result is `claim_not_current`; and when the caller passes `expected_authority_id` the claim must name exactly that id, otherwise the result is `wrong_authority_id`. The id check is off unless the id is passed, so callers should pass it. Successful verification means only `non_authorizing_digest_custody`.

## Documentation

The [documentation index](docs/README.md) lists every page in this repository, labelled current, historical or legacy. Start with the [verification contract](docs/VERIFICATION_CONTRACT_V1.md), then [ADR 001](docs/ADR-001-verification-boundary.md) and the [custody profile](docs/AUTHORITY_DIGEST_CUSTODY_PROFILE_V1.md). The twelve root documents (whitepaper, protocol specification, architecture, API reference, threat model and others) describe the earlier prototype and are labelled in the index; they are kept as records and are not the v1 interface.

## Compatibility and selection

The [component lock](https://github.com/cogno-us/cognous-open-control-stack/blob/main/component-lock.json) pins this repository at `5b5077dafde2` (verification contract v1); `main` is ahead of it, and a newer commit here is not selected until the lock changes. <!-- pin-round: refresh the lock revision here --> Source acceptance, selection and deployment approval remain separate decisions. Legacy RSA helpers and unsigned ingestion are not the v1 accepted path. Dependencies are not pinned by this repository; [validation record](docs/VALIDATION_V1.md) lists the environment it was tested in.

Test results, run commentary and historical qualification records are maintained in the [central test hub](https://github.com/cogno-us/cognous-stack-qualification/blob/main/results/readme-commentary/index.md). Read them against their recorded source revisions.

## What it does not do (known limits)

| Label | Limit |
| --- | --- |
| known limit | A valid signature proves that the configured key signed those bytes. It does not show that no rows were omitted, that the signer is who the name says, or that the content is true. Verification is against the current trust snapshot only; historical as-of verification, signed portable receipts and caller-selected evaluation times are not provided. |
| known limit | The trust snapshot and the evaluation time are supplied by the operator. Issuer enrollment, secure time, snapshot distribution and anti-rollback are deployment work. |
| known limit | The custody profile's `observed_at` and issuance times are signed assertions. The profile is not a trusted timestamp authority or transparency log, and its independence checks are conservative synthetic checks, not proof of organizational independence. |
| known limit | The legacy prototype API (identity, governance, integration) is unauthenticated: identities are names and votes carry a fixed weight. The legacy privacy and platform-verification routes return 501 and carry no assurance. |
| proposed | Reputation scoring, clustering, damping and zero-knowledge threshold proofs appear in the legacy design documents as goals; none is implemented. |
| known limit | No production cryptographic review, CodeQL run or deployment is implied by the local tests. |

Review original artifacts and their exact source revisions before extending a claim to a new environment. A passing reference case is not a certification of an enterprise deployment.

## Contributing, security and attribution

[Contribution guidance](CONTRIBUTING.md) describes review and validation expectations; see also the [security policy](SECURITY.md), the [code of conduct](CODE_OF_CONDUCT.md) and the [changelog](CHANGELOG.md). Keep evidence-linked claims, preserve historical records and separate proposed features from accepted implementation.

See [LICENSE](LICENSE) and [attribution](NOTICE) for the existing terms and third-party scope. Developed by [Cognous](https://cogno.us); no licensing change is part of this documentation update. Repository renames: see the [rename map](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/repository-renames.md); package names, schema identifiers and retained producer identities are unchanged.

---

## Bibliography

Selected external sources from the October 2026 research review. These inform evaluation questions; they do not establish Cognous implementation, adoption, conformance or production qualification.

- [OWASP GenAI Security Project. *State of Agentic AI Security and Governance*, version 2.01 (June 2026)](https://genai.owasp.org/resource/state-of-agentic-ai-security-and-governance/). Security synthesis covering agent identity, delegated permissions, tool access and containment.
- [Alexander Barrett. *Boundary Blindness Under Artificial Intelligence: Early Cross-Industry Findings on the Missing Decision-Evidence Layer* (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7210798). Working paper on carrying the basis for reliance across organizational boundaries; proposed architecture, not a validated interoperability guarantee.
- [Mick Yang et al. *AI Epistemic Risks: Emerging Mechanisms & Evidence* (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6873005). Research synthesis on persuasion, cognitive offloading and feedback loops; context for evidence quality and independent judgment.

See the [research bibliography](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/research-bibliography.md) for review scope and source-verification limits.

<!-- Retained anchors for existing documentation links. -->
<a id="current-selection-historical-evidence-and-a-bounded-example"></a>
<a id="evidence-and-supported-scope"></a>
