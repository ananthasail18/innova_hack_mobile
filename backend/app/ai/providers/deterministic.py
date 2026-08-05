from typing import List, Dict, Any, Optional
from app.ai.providers.base import AssistantProvider

class DeterministicProvider(AssistantProvider):
    def generate_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Any] = None
    ) -> Dict[str, Any]:
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

        if response_format:
            try:
                return {"parsed": response_format()}
            except Exception:
                pass

        return {
            "content": fallback_msg,
            "tool_calls": []
        }
