"""Pytest configuration and shared fixtures for API tests"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for testing the FastAPI app.
    
    The TestClient allows us to make HTTP requests to the app without running
    a live server. Each test gets its own client instance.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture that provides a test email for signup/unregister tests"""
    return "test.student@mergington.edu"


@pytest.fixture
def valid_activity_names():
    """Fixture providing all valid activity names from the app"""
    return [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Band",
        "Debate Club",
        "Science Club"
    ]
