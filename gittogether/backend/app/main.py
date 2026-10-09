from collections import Counter

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from .config import settings
from .db import Base, engine, get_db
from .models import Profile
from .schemas import Availability, ProfileCreate, ProfileOut, ProfileUpdate, SkillCount, StatsOut

app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.on_event("startup")
def startup():
    # Production containers run Alembic before Uvicorn; create_all keeps tests self-contained.
    Base.metadata.create_all(bind=engine)

def split_skills(raw: str) -> list[str]:
    return [s.strip() for s in raw.split(",") if s.strip()]

def to_out(profile: Profile) -> ProfileOut:
    """Serialize a profile, withholding skills and LinkedIn for LIMITED profiles."""
    hidden = profile.visibility == "LIMITED"
    return ProfileOut(
        id=profile.id,
        name=profile.name,
        bio=profile.bio,
        skills=[] if hidden else split_skills(profile.skills),
        linkedin_url="" if hidden else profile.linkedin_url,
        department=profile.department,
        year=profile.year,
        availability=profile.availability,
        visibility=profile.visibility,
        hidden=hidden,
        created_at=profile.created_at,
    )

def get_or_404(db: Session, profile_id: int) -> Profile:
    profile = db.get(Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.get("/")
def root():
    return {"service": settings.app_name, "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "UP"}

@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(select(func.count(Profile.id)))
    return {"status": "READY"}

@app.get("/api/profiles", response_model=list[ProfileOut])
def list_profiles(
    skill: str | None = Query(default=None, max_length=40),
    q: str | None = Query(default=None, max_length=80),
    availability: Availability | None = None,
    db: Session = Depends(get_db),
):
    query = select(Profile).order_by(Profile.id.desc())
    if availability:
        query = query.where(Profile.availability == availability)
    if skill:
        # Only PUBLIC skills are searchable, otherwise a search would reveal hidden skills.
        query = query.where(Profile.visibility == "PUBLIC", Profile.skills.ilike(f"%{skill.strip()}%"))
    if q:
        term = f"%{q.strip()}%"
        query = query.where(or_(Profile.name.ilike(term), Profile.department.ilike(term)))
    return [to_out(p) for p in db.scalars(query)]

@app.get("/api/profiles/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    rows = db.execute(select(Profile.availability, func.count(Profile.id)).group_by(Profile.availability)).all()
    counts = {availability: count for availability, count in rows}
    limited = db.scalar(select(func.count(Profile.id)).where(Profile.visibility == "LIMITED"))
    skill_counter = Counter()
    for raw in db.scalars(select(Profile.skills).where(Profile.visibility == "PUBLIC")):
        skill_counter.update(s.lower() for s in split_skills(raw))
    return StatsOut(
        total=sum(counts.values()),
        openToTeam=counts.get("OPEN_TO_TEAM", 0),
        busy=counts.get("BUSY", 0),
        notLooking=counts.get("NOT_LOOKING", 0),
        limited=limited,
        topSkills=[SkillCount(skill=s, count=c) for s, c in skill_counter.most_common(8)],
    )

@app.get("/api/profiles/{profile_id}", response_model=ProfileOut)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    return to_out(get_or_404(db, profile_id))

@app.post("/api/profiles", response_model=ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["skills"] = ", ".join(data["skills"])
    profile = Profile(**data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return to_out(profile)

@app.put("/api/profiles/{profile_id}", response_model=ProfileOut)
def update_profile(profile_id: int, payload: ProfileUpdate, db: Session = Depends(get_db)):
    profile = get_or_404(db, profile_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        if key == "skills":
            value = ", ".join(value or [])
        if key == "linkedin_url" and value is None:
            value = ""
        setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return to_out(profile)

@app.delete("/api/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    db.delete(get_or_404(db, profile_id))
    db.commit()
