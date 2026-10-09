import re
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, field_validator

Availability = Literal["OPEN_TO_TEAM", "BUSY", "NOT_LOOKING"]
Visibility = Literal["PUBLIC", "LIMITED"]

MAX_SKILLS = 15
LINKEDIN_RE = re.compile(r"^https://(www\.)?linkedin\.com/in/[A-Za-z0-9_%-]+/?$")

def clean_skills(value: list[str] | str | None) -> list[str] | None:
    """Accept a list or a comma-separated string; trim, drop blanks and case-insensitive duplicates."""
    if value is None:
        return None
    items = value.split(",") if isinstance(value, str) else value
    seen, result = set(), []
    for item in items:
        skill = item.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            result.append(skill[:40])
    if len(result) > MAX_SKILLS:
        raise ValueError(f"at most {MAX_SKILLS} skills allowed")
    return result

def check_linkedin(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if value and not LINKEDIN_RE.match(value):
        raise ValueError("must look like https://www.linkedin.com/in/your-name")
    return value

class ProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    bio: str = Field(default="", max_length=500)
    skills: list[str] = []
    linkedin_url: str = ""
    department: str = Field(default="", max_length=80)
    year: int | None = Field(default=None, ge=1, le=6)
    availability: Availability = "OPEN_TO_TEAM"
    visibility: Visibility = "PUBLIC"

    _skills = field_validator("skills", mode="before")(clean_skills)
    _linkedin = field_validator("linkedin_url")(check_linkedin)

class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    bio: str | None = Field(default=None, max_length=500)
    skills: list[str] | None = None
    linkedin_url: str | None = None
    department: str | None = Field(default=None, max_length=80)
    year: int | None = Field(default=None, ge=1, le=6)
    availability: Availability | None = None
    visibility: Visibility | None = None

    _skills = field_validator("skills", mode="before")(clean_skills)
    _linkedin = field_validator("linkedin_url")(check_linkedin)

class ProfileOut(BaseModel):
    id: int
    name: str
    bio: str
    skills: list[str]
    linkedin_url: str
    department: str
    year: int | None
    availability: Availability
    visibility: Visibility
    hidden: bool  # True when skills/LinkedIn were withheld because the profile is LIMITED
    created_at: datetime

class SkillCount(BaseModel):
    skill: str
    count: int

class StatsOut(BaseModel):
    total: int
    openToTeam: int
    busy: int
    notLooking: int
    limited: int
    topSkills: list[SkillCount]
