import pytest
import os
from app.ai.providers.gemini import GeminiProvider
from app.config.config import settings
from unittest.mock import patch, MagicMock
from openai import APIConnectionError

def test_missing_gemini_key():
    with patch.object(settings, 'GEMINI_API_KEY', None), patch.dict(os.environ, {}, clear=True):
        provider = GeminiProvider()
        # Even with missing key, fallback engine should guarantee valid response
        result = provider.generate_completion(messages=[{"role": "user", "content": "hello"}])
        assert "Hello!" in result["content"] or "recommend" in result["content"]

def test_invalid_gemini_key():
    with patch.object(settings, 'GEMINI_API_KEY', "invalid_key"):
        provider = GeminiProvider()
        result = provider.generate_completion(messages=[{"role": "user", "content": "hello"}])
        # Invalid key triggers fallback or informative API missing message
        assert "API_KEY" in result["content"] or "API key" in result["content"]

def test_gemini_timeout():
    with patch.object(settings, 'GEMINI_API_KEY', "dummy_key"):
        provider = GeminiProvider()
        
        # Simulate timeout by raising an exception in client.chat.completions.create
        with patch.object(provider.client.chat.completions, 'create', side_effect=Exception("Timeout")):
            result = provider.generate_completion(messages=[{"role": "user", "content": "hello"}])
            assert "recommend" in result["content"].lower() or "hello" in result["content"].lower()

def test_rate_limit_fallback():
    with patch.object(settings, 'GEMINI_API_KEY', "dummy_key"):
        provider = GeminiProvider()
        
        # Simulate rate limit 429
        with patch.object(provider.client.chat.completions, 'create', side_effect=Exception("429 Resource exhausted")):
            result = provider.generate_completion(messages=[{"role": "user", "content": "I am hungry"}])
            # Must return the smart fallback
            assert result["tool_calls"] == []
            assert isinstance(result["content"], str)
