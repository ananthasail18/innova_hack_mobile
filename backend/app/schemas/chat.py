from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ChatMessageRequest(BaseModel):
    message: str
    user_id: str
    restaurant_id: str
    page_context: str
    selected_dish_id: Optional[str] = None
    conversation_history: List[Dict[str, Any]] = []

class ToolCallSchema(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any]

class ChatResponse(BaseModel):
    message: Optional[str] = None
    tool_calls: List[ToolCallSchema] = []
    citations: List[str] = []
    confidence: float = 1.0
    follow_up_questions: List[str] = []
    updated_ui_actions: List[Dict[str, Any]] = []
    execution_mode: str = "LIVE_AI"
    recommendations: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}
