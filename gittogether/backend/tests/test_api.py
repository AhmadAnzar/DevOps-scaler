import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import engine, Base
from app import models  # ensure all models are registered with Base

@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    """Create all tables before the test session and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clean_profiles():
    """Each test starts with an empty profiles table."""
    with engine.begin() as conn:
        conn.execute(models.Profile.__table__.delete())

client = TestClient(app)

def make_profile(**overrides):
    payload = {
        "name": "Ayesha Khan",
        "bio": "Backend dev looking for a hackathon team",
        "skills": ["Python", "FastAPI", "Docker"],
        "linkedin_url": "https://www.linkedin.com/in/ayesha-khan",
        "department": "CSE",
        "year": 3,
        "availability": "OPEN_TO_TEAM",
        "visibility": "PUBLIC",
    }
    payload.update(overrides)
    response = client.post("/api/profiles", json=payload)
    assert response.status_code == 201, response.text
    return response.json()

def test_health():
    assert client.get("/health").json() == {"status": "UP"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "GitTogether API"

def test_create_profile():
    profile = make_profile()
    assert profile["id"] > 0
    assert profile["skills"] == ["Python", "FastAPI", "Docker"]
    assert profile["hidden"] is False

def test_skills_are_trimmed_and_deduplicated():
    profile = make_profile(skills=" React, react ,Figma,, ")
    assert profile["skills"] == ["React", "Figma"]

def test_rejects_invalid_linkedin_url():
    response = client.post("/api/profiles", json={"name": "Bob", "linkedin_url": "https://evil.example.com/bob"})
    assert response.status_code == 422

def test_rejects_empty_name():
    assert client.post("/api/profiles", json={"name": ""}).status_code == 422

def test_list_profiles_newest_first():
    make_profile(name="First")
    make_profile(name="Second")
    names = [p["name"] for p in client.get("/api/profiles").json()]
    assert names == ["Second", "First"]

def test_filter_by_skill_and_availability():
    make_profile(name="Py Dev", skills=["Python"])
    make_profile(name="Designer", skills=["Figma"], availability="BUSY")
    by_skill = client.get("/api/profiles", params={"skill": "python"}).json()
    assert [p["name"] for p in by_skill] == ["Py Dev"]
    busy = client.get("/api/profiles", params={"availability": "BUSY"}).json()
    assert [p["name"] for p in busy] == ["Designer"]

def test_get_profile_and_404():
    profile = make_profile()
    assert client.get(f"/api/profiles/{profile['id']}").json()["name"] == "Ayesha Khan"
    assert client.get("/api/profiles/99999").status_code == 404

def test_update_profile():
    profile = make_profile()
    response = client.put(f"/api/profiles/{profile['id']}", json={"availability": "BUSY", "skills": ["Go"]})
    assert response.status_code == 200
    assert response.json()["availability"] == "BUSY"
    assert response.json()["skills"] == ["Go"]
    assert response.json()["name"] == "Ayesha Khan"  # untouched fields are kept

def test_delete_profile():
    profile = make_profile()
    assert client.delete(f"/api/profiles/{profile['id']}").status_code == 204
    assert client.get(f"/api/profiles/{profile['id']}").status_code == 404

def test_limited_profile_hides_skills_and_linkedin():
    profile = make_profile(visibility="LIMITED")
    assert profile["hidden"] is True
    assert profile["skills"] == []
    assert profile["linkedin_url"] == ""
    fetched = client.get(f"/api/profiles/{profile['id']}").json()
    assert fetched["skills"] == [] and fetched["linkedin_url"] == ""

def test_limited_skills_are_not_searchable():
    make_profile(name="Shy Student", skills=["Rust"], visibility="LIMITED")
    assert client.get("/api/profiles", params={"skill": "rust"}).json() == []

def test_stats():
    make_profile(skills=["Python", "Docker"])
    make_profile(skills=["python"], availability="BUSY")
    make_profile(skills=["Rust"], availability="NOT_LOOKING", visibility="LIMITED")
    stats = client.get("/api/profiles/stats").json()
    assert stats["total"] == 3
    assert stats["openToTeam"] == 1 and stats["busy"] == 1 and stats["notLooking"] == 1
    assert stats["limited"] == 1
    assert stats["topSkills"][0] == {"skill": "python", "count": 2}
    assert all(s["skill"] != "rust" for s in stats["topSkills"])
