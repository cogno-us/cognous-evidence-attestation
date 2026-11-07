"""TEST-SCOPE ONLY signing support for the Verifier-result profile (development).

A fresh Ed25519 key is generated for each call and exists only in memory: nothing is written, logged,
committed or placed in any configuration. The snapshot it returns is a per-run synthetic trust snapshot
for the development audience, handed only to native verification. Production code never imports this.
"""
import base64

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from models.verification import SignedStatement
from profiles.verifier_result import AUDIENCE
from utils.verification import canonical_bytes

ISSUER = "issuer:synthetic-dev-run"
KEY_ID = "key:ephemeral-1"


def ephemeral_signer(now: int, **key_overrides) -> tuple[Ed25519PrivateKey, dict]:
    key = Ed25519PrivateKey.generate()
    public = key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    entry = {"issuer": ISSUER, "key_id": KEY_ID, "public_key": base64.b64encode(public).decode(),
             "valid_from": now - 60, "valid_until": now + 3600, "revoked_at": None}
    entry.update(key_overrides)
    registry = {"registry_version": "bitrep-trust/1", "audience": AUDIENCE,
                "published_at": now - 60, "valid_until": now + 3600, "keys": [entry]}
    return key, registry


def sign(key: Ed25519PrivateKey, statement: SignedStatement) -> dict:
    return {"statement": statement.model_dump(),
            "signature": base64.b64encode(key.sign(canonical_bytes(statement))).decode()}
