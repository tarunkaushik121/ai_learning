
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

URL = "/api/v1/interviews/start"


def test_start_interview_success():
    response = client.post(
        URL,
        json={
            "topic": "Java 8",
            "experience_level": "5 years",
            "difficulty": "Intermediate"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "started"
    assert data["topic"] == "Java 8"
    assert data["question_number"] == 1
    assert "thread_id" in data
    assert "question" in data


def test_numeric_easy():
    response = client.post(
        URL,
        json={
            "topic": "Java 8",
            "experience_level": "5 years",
            "difficulty": 1
        }
    )

    assert response.status_code == 201


def test_text_easy():
    response = client.post(
        URL,
        json={
            "topic": "Java 8",
            "experience_level": "5 years",
            "difficulty": "easy"
        }
    )

    assert response.status_code == 201


def test_medium():
    response = client.post(
        URL,
        json={
            "topic": "Spring Boot",
            "experience_level": "5 years",
            "difficulty": "medium"
        }
    )

    assert response.status_code == 201


def test_invalid_difficulty():
    response = client.post(
        URL,
        json={
            "topic": "Java 8",
            "experience_level": "5 years",
            "difficulty": "Expert"
        }
    )

    assert response.status_code == 422


def test_blank_topic():
    response = client.post(
        URL,
        json={
            "topic": " ",
            "experience_level": "5 years",
            "difficulty": "easy"
        }
    )

    assert response.status_code == 422
