from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Rank(Enum):
    CADET = "CADET"
    OFFICER = "OFFICER"
    LIEUTENANT = "LIEUTENANT"
    CAPTAIN = "CAPTAIN"
    COMMANDER = "COMMANDER"


# • member_id: String, 3-10 characters
# • name: String, 2-50 characters
# • rank: Rank enum
# • age: Integer, 18-80 years
# • specialization: String, 3-30 characters
# • years_experience: Integer, 0-50 years
# • is_active: Boolean, defaults to True
class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


# Mission with crew list and these fields:
# • mission_id: String, 5-15 characters
# • mission_name: String, 3-100 characters
# • destination: String, 3-50 characters
# • launch_date: DateTime
# • duration_days: Integer, 1-3650 days (max 10 years)
# • crew: List of CrewMember, 1-12 members
# • mission_status: String, defaults to "planned"
# • budget_millions: Float, 1.0-10000.0 million dollars
class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(default_factory=list, min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1, le=10000)

    @model_validator(mode="after")
    def validate(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if self.crew:
            found = False
            for cr in self.crew:
                if cr.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                    found = True
                    break
            if not found:
                raise ValueError("Must have at least one Commander or Captain")

        if self.duration_days > 365:
            crew_h_exp = 0
            for cr in self.crew:
                if cr.years_experience > 5:
                    crew_h_exp += 1
            if crew_h_exp * 2 < len(self.crew):
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew (5+ years)"
                )

        if self.crew:
            for cr in self.crew:
                if cr.is_active == False:
                    raise ValueError("All crew members must be active")


if __name__ == "__main__":
    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 6, 1, 10, 0, 0),
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=45,
                specialization="Mission Command",
                years_experience=20,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=38,
                specialization="Navigation",
                years_experience=12,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=32,
                specialization="Engineering",
                years_experience=8,
                is_active=True,
            ),
        ],
    )

    print(f"""
Space Mission Crew Validation
=========================================
Valid mission created:
Mission: {valid_mission.mission_name}
ID: {valid_mission.mission_id}
Destination: {valid_mission.destination}
Duration: {valid_mission.duration_days} days
Budget: ${valid_mission.budget_millions}M
Crew size: {len(valid_mission.crew)}
Crew members:""")

    for member in valid_mission.crew:
        print(
            f"- {member.name} ({member.rank.value.lower()}) - {member.specialization}"
        )

    try:
        print("=========================================")
        print("Expected validation error:")

        invalid_mission = SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Moon Base Alpha",
            destination="Moon",
            launch_date=datetime(2024, 8, 1, 10, 0, 0),
            duration_days=180,
            budget_millions=500.0,
            crew=[
                CrewMember(
                    member_id="CM004",
                    name="Bob Williams",
                    rank=Rank.OFFICER,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM005",
                    name="Jane Doe",
                    rank=Rank.CADET,
                    age=25,
                    specialization="Research",
                    years_experience=2,
                    is_active=True,
                ),
            ],
        )
    except ValidationError as e:
        print("Mission must have at least one Commander or Captain")
