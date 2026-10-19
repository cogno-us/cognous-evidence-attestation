from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AttestationIn(BaseModel):
    issuer: str
    subject: str
    attestation_type: str
    signature: Optional[str] = None
    anchor: Optional[str] = None

class AttestationOut(BaseModel):
    id: int
    issuer: str
    subject: str
    attestation_type: str
    timestamp: datetime
    signature: Optional[str] = None
    anchor: Optional[str] = None

    model_config = {"from_attributes": True}

class UserIdentity(BaseModel):
    username: str
    public_key: str
    verified: bool = False

class UserIdentityCreate(BaseModel):
    username: str
