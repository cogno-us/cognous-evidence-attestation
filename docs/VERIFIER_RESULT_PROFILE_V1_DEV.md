# Verifier-result attestation profile (development only)

Status: **development only, proposed, non-authorizing.** An additive profile over the unchanged `bitrep-attestation/1` contract. Profile id `cognous-verifier-result-attestation/1`. It is not a production signer, trust anchor or Registry integration, and it is not independent qualification.

## What it does
Given the exact bytes of an `evidence-pack-verification/0.1.0-dev` report (from the Verifier, `python -m cognous_verify.pack_cli PACK.json --out REPORT.json`), `profiles/verifier_result.py`:
1. builds an **unsigned** statement (`build_unsigned_statement`), and
2. checks a separately signed envelope against the report bytes and an explicitly supplied trust snapshot (`verify_verifier_result`): native signature/trust/time verification first, then the profile bindings.

Admission and readback use the existing `POST /attest` and `GET /attestations/{statement_digest}` unchanged.

## Statement mapping (all fields are signed)
| Field | Value |
|---|---|
| `statement_type` | `cognous.verifier-result.dev/1` (profile-local, not Registry-governed) |
| `audience` | `cognous-ocs-vnext-s4-dev` (must equal the snapshot audience) |
| `content_digest` | `sha256:` of the **exact report bytes** (nothing parsed or reserialized first) |
| `subject` | the report's declared `subject.digest` (digest of the Evidence Pack file) |
| `attestation_id` | `cognous-vr-dev/1/rev-<40 hex Verifier revision>/<64 hex report sha256>`: the signed binding of the developer-asserted Verifier revision |
| times | `issued_at = not_before = now`, `expires_at = now + 900` |

`statement_digest` (native, used for readback) is distinct from `content_digest`.

## Refusals
Report not strict JSON; wrong contract/version; not `development_only`; `overall` not reject/abstain/unsupported (an `accept` is refused); bad subject digest; bad revision; statement type, audience or id convention mismatch; content digest not the hash of the supplied bytes; subject mismatch; window over 900 s. Native refusals (`invalid_signature`, `unknown_key`, `key_revoked`, `audience_mismatch`, expiry, …) pass through unchanged. Missing or expired trust raises `TrustUnavailable`; there is no result.

## Boundaries
- The module never signs, loads or creates keys, enrolls issuers or stores anything. Development signing exists only in `tests/verifier_result_signing.py`, with a fresh in-memory Ed25519 key and a per-run snapshot; nothing is persisted or committed.
- The v1 statement has no verdict field. The Verifier outcome is bound only via `content_digest` and is re-read from the report bytes, unchanged (an `abstain` stays `abstain`).
- The Verifier revision is a caller assertion, not authenticated source identity.
- `accepted` and `issuer_signature_only` mean only that the enrolled key signed these statement bytes. **Not verified:** report correctness, Evidence Pack genuineness, that execution occurred, Verifier-revision authenticity, signer authority, independent custody or qualification.
- Readback re-evaluates against the current trust snapshot, so a later expiry or revocation turns it into `rejected`.

Rollback: delete `profiles/verifier_result.py`, `tests/verifier_result_signing.py`, `tests/test_verifier_result_profile.py`, `tests/fixtures/verifier-result/` and this page (plus its docs index row).
