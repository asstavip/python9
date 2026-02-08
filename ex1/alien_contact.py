from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = "RADIO"
    VISUAL = "VISUAL"
    PHYSICAL = "PHYSICAL"
    TELEPATHIC = "TELEPATHIC"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0, le=10)
    duration_minutes: int = Field(ge=1, le=1440)
    message_received: Optional[str] = Field(default=None, max_length=500)
    witness_count: int = Field(ge=1, le=100)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")
        if not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        is_eq = self.contact_type == ContactType.TELEPATHIC
        if is_eq and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
                )
        return self


valid_contact = AlienContact(
    contact_id="AC_2024_001",
    timestamp=datetime(2024, 1, 15, 22, 30, 0),
    location="Area 51, Nevada",
    contact_type=ContactType.RADIO,
    signal_strength=8.5,
    duration_minutes=45,
    witness_count=5,
    message_received="Greetings from Zeta Reticuli",
    is_verified=True,
)
print(f"""
Alien Contact Log Validation
======================================
Valid contact report:
ID: {valid_contact.contact_id}
Type: {valid_contact.contact_type}
Location: {valid_contact.location}
Signal: {valid_contact.signal_strength}/10
Duration: {valid_contact.duration_minutes} minutes
Witnesses: {valid_contact.witness_count}
Message: {valid_contact.message_received}""")
try:
    print("======================================")

    not_valid = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 1, 15, 22, 30, 0),
        location="Area 51, Nevada",
        contact_type=ContactType.TELEPATHIC,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=2,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )
except ValidationError as e:
    print("Validation error:", e)
