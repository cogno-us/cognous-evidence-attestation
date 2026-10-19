# Evidence Attestation documentation index

Every page in this repository is listed here once. Labels: **current** (describes the selected v1 interface or a profile on top of it), **proposed** (a bounded optional proposal), **historical** (a dated record kept as written), **legacy** (describes the earlier prototype, not the v1 interface; read it with the status banner at its top). Back to the [repository README](../README.md). Stack-level scope and limits are stated once in the hub [guarantees and limits](https://github.com/cogno-us/cognous-open-control-stack/blob/main/docs/guarantees-and-limits.md) page.

A successful v1 verification means `issuer_signature_only`: the configured key signed those exact bytes at the evaluation time under the operator's trust snapshot. It does not establish truth, the signer's real identity or authority.

## The v1 interface

| Page | Label | What it is |
| --- | --- | --- |
| [Verification contract v1](VERIFICATION_CONTRACT_V1.md) | current | Wire format, canonical signed bytes, trust snapshot, time rules, admission and the limits. It keeps its original proposal-stage header; the hub lock records what is selected. |
| [ADR 001: versioned admission with explicit issuer trust](ADR-001-verification-boundary.md) | current | Why v1 is Ed25519-only with an operator-managed issuer-key snapshot and a separate accepted-record table. |
| [Verification workstream validation](VALIDATION_V1.md) | historical | The commands and results recorded when v1 was validated (81 tests at that time; the suite now has more). |
| [Attestation schema](attestation-v1.schema.json) | current | JSON Schema of the signed envelope. |
| [Trust snapshot schema](trust-v1.schema.json) | current | JSON Schema of the operator trust snapshot. |
| [Verification result schema](verification-v1.schema.json) | current | JSON Schema of the result. |

## Optional profile

| Page | Label | What it is |
| --- | --- | --- |
| [Authority digest custody profile v1](AUTHORITY_DIGEST_CUSTODY_PROFILE_V1.md) | proposed | Publisher claim plus an independent witness commitment over an authority digest; result `non_authorizing_digest_custody`. Includes the effective-interval and optional expected-id checks. |
| [Custody claim schema](authority-digest-custody-v1.schema.json) | proposed | JSON Schema of the claim. |

## Security, governance and contribution

| Page | Label | What it is |
| --- | --- | --- |
| [Security policy](../SECURITY.md) | current | Scope and how to report. Its v1 statements: Ed25519 for v1; RSA helpers are legacy only. |
| [Contributing](../CONTRIBUTING.md) | current | Contribution expectations and the test command. |
| [Code of conduct](../CODE_OF_CONDUCT.md) | current | Community expectations. |
| [Changelog](../CHANGELOG.md) | current | Change list, starting with the v1 contract. |
| [Developer setup](../DEVELOPER_SETUP.md) | current | Clone, install, test and run the service; trust configuration. |

## Legacy prototype documents (earlier design, not the v1 interface)

These describe the earlier BitRep prototype: client-side RSA identities, reputation scoring, governance voting and privacy proofs. Several describe goals that are not implemented. The identity, governance, integration and privacy routes still exist as a legacy prototype API; they are unauthenticated and carry no assurance.

| Page | Label | What it is |
| --- | --- | --- |
| [Threat model](../THREAT_MODEL.md) | legacy | Threats and mitigations for the prototype; its "Current Implementation Limits" section states what the legacy API does not do. |
| [Protocol specification](../PROTOCOL_SPEC.md) | legacy | The prototype protocol; legacy items are marked in it. |
| [Architecture](../ARCHITECTURE.md) | legacy | The five-layer prototype design; goals marked "not implemented" are proposals. |
| [API reference](../API_REFERENCE.md) | historical | An earlier design; its banner says most routes do not exist. |
| [API documentation](../API_DOCUMENTATION.md) | legacy | Prototype API description. |
| [Implementation summary](../IMPLEMENTATION_SUMMARY.md) | historical | Summary of an earlier implementation plan; its banner states which items are absent. |
| [Integrations](../INTEGRATIONS.md) | legacy | Third-party import design; the platform-verification route returns 501. |
| [Governance model](../GOVERNANCE.md) | legacy | Reputation-weighted voting design; not part of v1. |
| [Roadmap](../ROADMAP.md) | legacy | Early plan; not a commitment. |
| [Whitepaper](../BitRep_Whitepaper.md) | historical | The original peer-to-peer reputation paper. |

## Overviews

| Page | What it is |
| --- | --- |
| [Business overview](../collateral/business-collateral.md) | Non-technical introduction to this component's role and limits. |
| [One-page overview](../collateral/one-page-overview.md) | One-page version. Neither page describes extra features. |
