import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from app.ai.providers.base import AssistantProvider
from app.config.config import settings
import logging

logger = logging.getLogger(__name__)

class GeminiProvider(AssistantProvider):
    def __init__(self):
        # We assume settings.GEMINI_API_KEY is available or os.environ has it
        api_key = getattr(settings, "GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
        if not api_key:
            logger.warning("GEMINI_API_KEY not found. LLM calls will fail.")
            
        if api_key and api_key.startswith("gsk_"):
            base_url = "https://api.groq.com/openai/v1"
            model_name = "llama-3.3-70b-versatile"
        else:
            base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
            model_name = "gemini-2.5-flash"

        self.api_key = api_key
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key or "DUMMY_KEY_FOR_TESTS",
            timeout=3.0,
            max_retries=0
        )
        self.model_name = model_name

    def generate_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Any] = None
    ) -> Dict[str, Any]:
        from app.ai.providers.base import ProviderUnavailableError
        
        params = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            params["tools"] = tools

        try:
            if response_format:
                response = self.client.beta.chat.completions.parse(**params, response_format=response_format)
                return {"parsed": response.choices[0].message.parsed}
            else:
                response = self.client.chat.completions.create(**params)
                choice = response.choices[0].message
                
                result = {
                    "content": choice.content,
                    "tool_calls": []
                }
                
                if choice.tool_calls:
                    for tc in choice.tool_calls:
                        result["tool_calls"].append({
                            "id": tc.id,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        })
                        
                return result
            
        except Exception as e:
            logger.warning(f"GeminiProvider attempt failed: {e}")
            raise ProviderUnavailableError(f"Gemini provider unavailable: {e}")

