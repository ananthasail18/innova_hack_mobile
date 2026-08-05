from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class AssistantProvider(ABC):
    @abstractmethod
    def generate_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        response_format: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a completion from the LLM.
        Should return a standard OpenAI-like response dictionary with:
        {
            "content": str,
            "tool_calls": [
                {
                    "id": str,
                    "function": {
                        "name": str,
                        "arguments": str (JSON string)
                    }
                }
            ]
        }
        """
        pass

