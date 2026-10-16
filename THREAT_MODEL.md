# BitRep Threat Model

This document outlines the threat model for BitRep’s identity, attestation, reputation, and governance layers. It defines what the system defends against, what it does not, and the assumptions underlying the protocol.

## Security Goals
- ensure identities cannot be forged
- ensure attestations cannot be tampered with
- ensure reputation scores are deterministic and auditable
- limit the impact of Sybil attacks (design goal; **not met** by the prototype governance API, see [Current Implementation Limits](#current-implementation-limits))
- prevent unauthorized modification of proposals, votes, or tallies (design goal; **not met** by the prototype governance API, see [Current Implementation Limits](#current-implementation-limits))
- avoid leaking sensitive graph structure where possible

## Out-of-Scope Goals
BitRep does not attempt to:
- guarantee privacy of raw reputation scores
- prevent metadata leakage from network traffic
- secure client devices or key storage
- enforce honest behavior from issuers
- prevent denial-of-service attacks
- provide production-grade zero-knowledge privacy

## Assets
- identity keypairs
- attestation records
- trust graph structure
- reputation scores and caches
- governance proposals and votes
- API request/response integrity

## Adversary Capabilities
Attackers may:
- create unlimited identities (Sybil capability)
- issue arbitrary attestations
- attempt to manipulate reputation scores
- observe network traffic
- compromise storage or logs
- submit malicious API payloads
- attempt to dominate governance proposals

Attackers are *not* assumed to:
- break RSA-2048
- compromise the server runtime environment
- intercept private keys stored securely by users
- control a majority of all identities globally

## Threats and Mitigations

### Identity Forgery
**Threat:** attacker attempts to impersonate another identity.  
**Mitigation:** RSA signatures; deterministic verification; no shared secrets.

### Attestation Manipulation
**Threat:** attacker modifies or injects forged attestations.  
**Mitigation:** signatures on all attestations; strict validation; timestamp checks.

### Sybil Amplification
**Threat:** attacker creates many identities to inflate reputation.  
**Mitigation:** issuer-weight normalization; cluster detection; propagation damping.

### Graph Poisoning
**Threat:** attacker issues malicious attestations to distort trust graph.  
**Mitigation:** weighted propagation; issuer credibility; bounded influence.

### Governance Capture
**Threat:** attacker attempts to dominate voting.  
**Mitigation (design only, not implemented):** quadratic voting; reputation-weighted power; deterministic tallies. The prototype `POST /governance/vote` handler gives every existing identity a fixed weight of 1.0 and does not apply these mitigations.

### Privacy Leakage
**Threat:** attacker infers sensitive relationships from graph structure.  
**Mitigation:** coarse-grained score bands; optional ZK threshold proofs.

## Residual Risks
- large, coordinated Sybil clusters may still influence outcomes
- metadata leakage from API usage patterns
- ZK framework is experimental and not suitable for high-assurance privacy
- compromised client devices undermine identity security

## Assumptions
- cryptographic primitives remain secure
- server environment is not compromised
- contributors act in good faith unless proven otherwise
- users manage their private keys responsibly

## Current Implementation Limits
These limits describe the legacy prototype API in this repository. They do not affect the separate v1 verification contract.
- **Governance writes are unauthenticated.** `POST /governance/proposal` and `POST /governance/vote` accept a caller-supplied `proposer` or `voter` string and check only that the username exists. No key, signature or session binds the request to that identity, so any caller who can reach the API can create proposals or cast votes in another identity's name.
- **Unlimited identities mean unlimited votes.** `POST /identity/create` is a public operation, and the vote handler counts each existing identity as one vote of weight 1.0, whether or not that identity is verified. An attacker who creates many identities can decide prototype proposal outcomes. The prototype does not limit Sybil attacks and does not resist governance capture.
- **Integration records are unauthenticated and stay unverified.** `POST /integration/import` and `POST /integration/github/import` let any caller attach arbitrary platform data to an existing username. Rows are stored as pending (`verified=0`). The verification route returns 501, so callers cannot promote these records to verified, and they must not be treated as evidence about the named user.

## Summary
BitRep's design aims to resist identity forgery, attestation tampering, graph manipulation, and governance capture. The current prototype governance and integration APIs do not meet the governance-capture or Sybil goals (see [Current Implementation Limits](#current-implementation-limits)). BitRep does not attempt to solve client-side security, metadata privacy, or advanced adversarial coordination. This document does not claim that the system is secure or production-ready.
