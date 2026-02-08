from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from datetime import datetime

class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0, le=100)
    oxygen_level: float = Field(ge=0, le=100)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None,max_length=200)


s = SpaceStation(
    station_id="ISS001",
    name="International Space Station",
    crew_size=6,
    power_level=85.5,
    oxygen_level=92.3,
    is_operational=True,
    last_maintenance=datetime.now(),
)


print(f"""
Space Station Data Validation
========================================
Valid station created:
ID: {s.station_id}
Name: {s.name}
Crew: {s.crew_size} people
Power: {s.power_level}%
Oxygen: {s.oxygen_level}%
Status: {"Operational" if s.is_operational else "Not Operational"}
========================================""")

try:
    s = SpaceStation(
    station_id="ISS002",
    name="International Space Station",
    crew_size=30,
    power_level=15.2,
    oxygen_level=92.3,
    is_operational=True,
    last_maintenance=datetime.now(),
    )
except ValidationError as e:
    print(e)