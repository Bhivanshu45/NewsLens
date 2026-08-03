import uuid

from app.services.chat.schemas import ChatMessage
from app.services.chat.schemas import ChatRole
from app.services.chat.schemas import ConversationHistory


class ConversationService:

	def __init__(self):
		self._conversations: dict[str, ConversationHistory] = {}

	def create_conversation(self) -> str:
		conversation_id = str(uuid.uuid4())
		self._conversations[conversation_id] = ConversationHistory()
		return conversation_id

	def conversation_exists(
		self,
		conversation_id: str,
	) -> bool:
		return conversation_id in self._conversations

	def get_history(
		self,
		conversation_id: str,
	) -> ConversationHistory:
		if conversation_id not in self._conversations:
			self._conversations[conversation_id] = ConversationHistory()

		return self._conversations[conversation_id]

	def append_user_message(
		self,
		conversation_id: str,
		content: str,
	) -> None:
		history = self.get_history(conversation_id)
		history.messages.append(
			ChatMessage(
				role=ChatRole.USER,
				content=content,
			)
		)

	def append_assistant_message(
		self,
		conversation_id: str,
		content: str,
	) -> None:
		history = self.get_history(conversation_id)
		history.messages.append(
			ChatMessage(
				role=ChatRole.ASSISTANT,
				content=content,
			)
		)
