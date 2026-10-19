# Contributing to BitRep

BitRep is an open protocol and reference implementation for verifiable, portable reputation. Contributions are welcome across cryptography, backend engineering, graph algorithms, governance design, and privacy systems.

The accepted interface is the Ed25519 verification contract v1 ([README](README.md), [contract](docs/VERIFICATION_CONTRACT_V1.md)). Reputation scoring, graph scoring and zero-knowledge proofs below are legacy or proposed areas, not shipped features. Run `python -m pytest -q tests` before submitting.

## How to Contribute
- **open an issue** — report bugs, propose features, or start design discussions  
- **submit a pull request** — small, focused changes are easiest to review  
- **join a discussion** — comment on open issues or propose architectural improvements  

## Development Workflow
- **fork the repository** and create a feature branch  
- **write clear, minimal commits** with descriptive messages  
- **add or update tests** for any functional changes  
- **run the full test suite** before submitting a PR  
- **ensure API compatibility** unless the change is explicitly breaking  

## Code Standards
- **type‑annotate all functions**  
- **follow FastAPI conventions** for endpoints and responses  
- **document new modules** with concise docstrings  
- **avoid unnecessary dependencies** to keep the core lightweight  

## Security‑Related Contributions
- **do not open public issues for security concerns**  
- **email the maintainer privately** for any security concerns  
- **include reproduction steps** and affected components  
- **avoid speculative claims** — stick to demonstrable issues  

## What Makes a Good PR
- **small, self‑contained changes**  
- **clear motivation** in the PR description  
- **tests that cover edge cases**  
- **alignment with project architecture**  
- **no unrelated refactors** in functional PRs  

## Areas Where Help Is Most Needed
- **cryptographic review** of identity and attestation layers  
- **graph‑scoring improvements** to the reputation algorithm  
- **governance model refinement** for proposals and voting  
- **privacy enhancements** to the ZK framework  
- **integration adapters** for additional platforms  

## Community Expectations
- **be direct and constructive**  
- **focus on clarity over cleverness**  
- **respect architectural boundaries**  
- **assume good faith** in discussions  
