# BitRep Architecture

BitRep is a modular protocol for verifiable, portable reputation. The architecture is built around five core layers: identity, attestations, reputation, governance, and privacy. Each layer is independent but interoperable, allowing the system to evolve without centralization or monolithic coupling.

## Identity Layer
- cryptographic identities — RSA‑2048 keypairs generated client‑side
- public keys as identifiers — no usernames, no central registry
- verification endpoints — signatures validate identity ownership
- key rotation — identities can rotate keys without losing reputation

The identity layer provides the foundation for all attestations and trust relationships.

## Attestation Layer
- signed statements — identities issue attestations about others
- mutual validation — attestations include issuer, subject, weight, and signature
- Sybil‑resistant structure — clustering and issuer‑credibility weighting (design goal, not implemented)
- import adapters — GitHub, eBay, LinkedIn, StackOverflow

Attestations form the edges of the trust graph and are the primary input to reputation scoring.

## Reputation Layer
- trust graph — directed, weighted graph built from attestations
- propagation algorithm — modified PageRank with damping and issuer weighting (design goal, not implemented)
- Sybil resistance — cluster detection and weight normalization (design goal, not implemented)
- score bands — coarse‑grained outputs for privacy‑preserving use

Reputation is computed from the global graph, not from any single platform.

## Governance Layer
- proposal system — identities create proposals with metadata and deadlines
- reputation‑weighted voting — voting power derived from computed scores
- quadratic scaling — reduces dominance by high‑reputation identities
- tallying and validation — deterministic, verifiable results

Governance is optional but provides a decentralized decision‑making mechanism for communities using BitRep.

## Privacy Layer
- ZK framework — experimental, used for threshold proofs
- selective disclosure — reveal reputation bands without raw scores
- minimal‑leakage design — avoid exposing graph structure
- non‑production components — ZK system is for research, not deployment

The privacy layer allows users to prove they meet requirements without revealing sensitive data.

## API Architecture
- FastAPI service — modular routers for each subsystem
- identity endpoints — create, verify, rotate keys
- attestation endpoints — issue, validate, list
- reputation endpoints — compute, query, inspect graph
- governance endpoints — proposals, votes, tallies

The API is stateless aside from stored attestations and cached reputation scores.

## Data Model
- identities — public key, metadata, verification state
- attestations — issuer, subject, weight, signature, timestamp
- trust graph — adjacency lists with normalized weights
- reputation cache — computed scores with TTL
- governance objects — proposals, votes, tallies

All data structures are designed for auditability and deterministic recomputation.

## Security Model
- RSA signatures secure identity and attestations
- input validation on all endpoints
- no custom cryptography — only standard primitives
- documented threat model — Sybil, malicious issuers, graph manipulation
- ZK components experimental — not for production use

Security is enforced through cryptographic verification and graph‑level resistance, not trust in any central authority.
