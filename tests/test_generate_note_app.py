import pytest
from unittest.mock import Mock, patch
from app.utils.generate_note import generate_note

MOCK_INPUT = {
    "recipient_name": "John Doe",
    "recipient_headline": "Software Engineer at TechCorp",
    "recipient_about": "Experienced engineer with a passion for building scalable systems.",
    "purpose": "Connect to discuss collaboration opportunities.",
    "sender_name": "Alice",
}

MOCK_NOTE = (
    "Hi John Doe, I noticed your work as a Software Engineer at TechCorp and wanted to connect to discuss "
    "collaboration opportunities. Looking forward to engaging with you. Best, Alice."
)


def test_generate_note():
    with patch("app.utils.generate_note.client.completions.create") as mock_create:
        mock_create.return_value = Mock(choices=[Mock(text=MOCK_NOTE)])
        result = generate_note(Mock(**MOCK_INPUT))
        assert result == MOCK_NOTE
