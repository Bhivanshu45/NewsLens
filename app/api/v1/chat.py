from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import get_chat_service
from app.services.chat.chat_service import ChatService
from app.services.chat.schemas import ChatRequest
from app.services.chat.schemas import ChatResponse


router = APIRouter(
	prefix="/chat",
	tags=["Chat"]
)


@router.post(
	"",
	response_model=ChatResponse,
)
def chat(
	request: ChatRequest,
	service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
	return service.chat(request)
