import pytest
import os
from app.config.config import settings
from unittest.mock import patch, MagicMock
from openai import APIConnectionError
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_missing_gemini_key(client: TestClient):
    with patch.object(settings, 'GEMINI_API_KEY', None), patch.dict(os.environ, {}, clear=True):
        response = client.post("/api/v1/chat", json={
            "message": "hello",
            "conversation_history": [],
            "user_id": "1",
            "restaurant_id": "1", "page_context": "test"
        })
        data = response.json()
        assert data["execution_mode"] == "SERVER_DETERMINISTIC"
        assert ".env" not in data["data"]["message"]

def test_invalid_gemini_key(client: TestClient):
    with patch.object(settings, 'GEMINI_API_KEY', "invalid_key"):
        response = client.post("/api/v1/chat", json={
            "message": "hello",
            "conversation_history": [],
            "user_id": "1",
            "restaurant_id": "1", "page_context": "test"
        })
        data = response.json()
        assert data["execution_mode"] == "SERVER_DETERMINISTIC"
        assert ".env" not in data["data"]["message"]

def test_gemini_timeout(client: TestClient):
    with patch.object(settings, 'GEMINI_API_KEY', "dummy_key"):
        # Simulate timeout by raising an exception in client.chat.completions.create
        with patch('app.ai.providers.gemini.OpenAI') as MockOpenAI:
            mock_client = MockOpenAI.return_value
            mock_client.chat.completions.create.side_effect = Exception("Timeout")
            
            response = client.post("/api/v1/chat", json={
                "message": "hello",
                "conversation_history": [],
                "user_id": "1",
                "restaurant_id": "1",
                "page_context": "test"
            })
            data = response.json()
            assert data["execution_mode"] == "SERVER_DETERMINISTIC"
            assert ".env" not in data["data"]["message"]

def test_only_one_model_attempted():
    # Since we removed the loop in GeminiProvider, it will only attempt once and raise ProviderUnavailableError
    from app.ai.providers.gemini import GeminiProvider
    from app.ai.providers.base import ProviderUnavailableError
    with patch.object(settings, 'GEMINI_API_KEY', "dummy_key"):
        provider = GeminiProvider()
        with patch.object(provider.client.chat.completions, 'create', side_effect=Exception("Timeout")) as mock_create:
            with pytest.raises(ProviderUnavailableError):
                provider.generate_completion(messages=[{"role": "user", "content": "I am hungry"}])
            assert mock_create.call_count == 1
