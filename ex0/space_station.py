from pydantic import BaseModel, Field
from typing import Annotated,Literal
# station_id: String, 3-10 characters
# • name: String, 1-50 characters
# • crew_size: Integer, 1-20 people
# • power_level: Float, 0.0-100.0 percent
# • oxygen_level: Float, 0.0-100.0 percent
# • last_maintenance: DateTime field
# • is_operational: Boolean, defaults to True
# • notes: Optional string, max 200 characters

class SpaceStation(BaseModel):
    pass



# Space Station Data Validation
# ========================================
# Valid station created:
# ID: ISS001
# Name: International Space Station
# Crew: 6 people
# Power: 85.5%
# Oxygen: 92.3%
# Status: Operational
# ========================================
# Expected validation error:
# Input should be less than or equal to 20
def main():
    pass



if __name__ == "__main__":
    main()