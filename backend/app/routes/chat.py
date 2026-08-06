from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.chat import ChatMessageRequest, ChatResponse, ToolCallSchema
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.deterministic import DeterministicProvider
from app.ai.context.builder import ContextBuilder
from app.config.config import settings
from app.ai.prompt.builder import PromptBuilder
from app.ai.tools.definitions import get_tool_definitions
from app.ai.tools.executor import ToolExecutor
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/chat", response_model=dict)
def process_chat(request: ChatMessageRequest, db: Session = Depends(get_db)):
    try:
        # 1. Build Context
        context_builder = ContextBuilder(db)
        context = context_builder.build_context(
            user_id=request.user_id,
            restaurant_id=request.restaurant_id,
            page_context=request.page_context,
            selected_dish_id=request.selected_dish_id,
            query=request.message
        )
        
        # 2. Build Prompt
        prompt_builder = PromptBuilder()
        system_prompt = prompt_builder.build_system_prompt(context)
        
        # 3. Assemble Messages
        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.conversation_history:
            messages.append(msg)
            
        messages.append({"role": "user", "content": request.message})
        
        # 4. Call LLM
        provider = GeminiProvider() if getattr(settings, "AI_PROVIDER", "LIVE_AI") == "LIVE_AI" else DeterministicProvider()
        tools = get_tool_definitions()
        
        try:
            llm_response = provider.generate_completion(messages=messages, tools=tools)
        except Exception as e:
            from app.ai.providers.base import ProviderUnavailableError
            if isinstance(e, ProviderUnavailableError) or getattr(settings, "AI_PROVIDER", "LIVE_AI") == "LIVE_AI":
                logger.warning(f"Primary provider failed, falling back to DeterministicProvider: {e}")
                provider = DeterministicProvider()
                llm_response = provider.generate_completion(messages=messages, tools=tools)
            else:
                raise
        
        # 5. Process Tools
        tool_calls = []
        updated_ui_actions = []
        
        if llm_response.get("tool_calls"):
            import json
            for tc in llm_response["tool_calls"]:
                func = tc.get("function", {})
                name = func.get("name", "") if isinstance(func, dict) else ""
                args = func.get("arguments", {}) if isinstance(func, dict) else {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                if name:
                    tool_calls.append(ToolCallSchema(
                        id=tc.get("id", "call_1"),
                        name=name,
                        arguments=args if isinstance(args, dict) else {}
                    ))
                
            executor = ToolExecutor()
            updated_ui_actions = executor.execute(tool_calls)
            
        # 6. Format Response
        execution_mode = "LIVE_AI"
        if isinstance(provider, DeterministicProvider) or getattr(provider, 'api_key', '') == 'DUMMY_KEY_FOR_TESTS':
            execution_mode = "SERVER_DETERMINISTIC"

        recs = []
        # If deterministic, manually run RecommendationService
        if execution_mode == "SERVER_DETERMINISTIC":
            from app.services.recommendation import RecommendationService
            rec_service = RecommendationService(db)
            rec_resp = rec_service.get_recommendations(request.user_id, request.restaurant_id)
            recs = [r.model_dump() for r in rec_resp.recommendations]

        response_data = ChatResponse(
            message=llm_response.get("content"),
            tool_calls=tool_calls,
            updated_ui_actions=updated_ui_actions,
            execution_mode=execution_mode,
            recommendations=recs,
            metadata={"source": execution_mode}
        )
        
        return {"status": "success", "data": response_data.model_dump(), "execution_mode": execution_mode, "recommendations": recs, "metadata": {"source": execution_mode}}

    except Exception as e:
        print("CHAT ROUTE EXCEPTION DETECTED:", type(e), e, flush=True)
        logger.error(f"Error processing chat: {e}", exc_info=True)
        return {
            "status": "error", 
            "data": ChatResponse(
                message="I'm unable to answer that right now.",
                tool_calls=[],
                updated_ui_actions=[]
            ).model_dump()
        }


