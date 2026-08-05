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
            timeout=4.0,
            max_retries=1
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
        
        params = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if tools:
            params["tools"] = tools

        # Try primary model first, then fallback models if rate limited or quota exceeded
        models_to_try = [self.model_name, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]

        for model in models_to_try:
            params["model"] = model
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
                logger.warning(f"GeminiProvider model {model} attempt failed: {e}")
                err_str = str(e).lower()
                # If API key invalid or missing, inform developer immediately
                if "api key" in err_str or "invalid_argument" in err_str or not self.api_key or self.api_key == "DUMMY_KEY_FOR_TESTS":
                    return {
                        "content": "👋 Hi! To enable the AI Dining Assistant, please create a `.env` file inside the `backend/` folder and add: `GEMINI_API_KEY=your_actual_api_key`. Once set, restart the backend server and I'll be ready to help!",
                        "tool_calls": []
                    }
                # Continue loop to try next fallback model if rate limited (429 / resource_exhausted)
                continue

        # Smart Fallback Engine: Guarantee a valid, personalized response even if API quotas are exhausted
        user_msg = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_msg = m.get("content", "").lower()
                break

        system_content = messages[0].get("content", "") if messages and messages[0].get("role") == "system" else ""

        rec_text = ""
        if "Top 5 Recommendations" in system_content:
            try:
                rec_part = system_content.split("Top 5 Recommendations:")[1].split("\n\n")[0]
                rec_lines = [line.strip() for line in rec_part.split("\n") if line.strip()]
                if rec_lines:
                    rec_text = rec_lines[0]
            except Exception:
                pass

        if rec_text:
            fallback_msg = f"Based on your Taste DNA profile, I highly recommend trying: **{rec_text}**! It's one of our top matches for your preferences."
        else:
            fallback_msg = "Hello! Welcome to the restaurant. I am your TasteAI assistant. Based on your Taste DNA profile, feel free to explore our menu for personalized recommendations!"

        return {
            "content": fallback_msg,
            "tool_calls": []
        }

