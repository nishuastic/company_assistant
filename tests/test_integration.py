import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import Mock

client = TestClient(app)

MOCK_BASE_URL = "https://mocksite.com"
MOCK_ANALYZED_RESULT = {
    "https://mocksite.com/about-us": "About us content",
    "https://mocksite.com/pricing": "Pricing content",
}
MOCK_INPUT_NOTE = {
    "recipient_name": "John Doe",
    "recipient_headline": "Software Engineer at TechCorp",
    "recipient_about": "Experienced engineer with a passion for building scalable systems.",
    "purpose": "Connect to discuss collaboration opportunities.",
    "sender_name": "Alice",
}


def test_value_app_integration(mocker):
    # Mocking the processing and vectorstore creation
    mocker.patch(
        "app.utils.value_utils.process_value_app_logic",
        return_value=MOCK_ANALYZED_RESULT,
    )
    mock_vectorstore = Mock()
    mocker.patch(
        "app.utils.value_utils.create_langchain_context", return_value=mock_vectorstore
    )

    response = client.get("/value/analyze", params={"base_url": MOCK_BASE_URL})
    assert response.status_code == 200
    assert response.json()["base_url"] == MOCK_BASE_URL
    assert response.json()["filtered_content"] == MOCK_ANALYZED_RESULT


def test_linkedin_generator_integration(mocker):
    mocker.patch(
        "app.utils.generate_note.client.completions.create",
        return_value=Mock(choices=[Mock(text="Sample LinkedIn Note")]),
    )

    response = client.post("/linkedin/generate_note", json=MOCK_INPUT_NOTE)
    assert response.status_code == 200
    assert response.json()["note"] == "Sample LinkedIn Note"
