from app.services.chat.schemas import ChatRole
from app.services.chat.schemas import ConversationHistory


class RetrievalQueryBuilder:

	def build(
		self,
		history: ConversationHistory,
		current_query: str,
		max_previous_messages: int,
	) -> str:
		previous_user_messages = self._get_previous_user_messages(
			history=history,
			max_previous_messages=max_previous_messages,
		)

		if not previous_user_messages:
			return f"Current User Question:\n{current_query}"

		recent_questions = "\n".join(
			f"- {message}"
			for message in previous_user_messages
		)

		return (
			"Recent User Questions:\n"
			f"{recent_questions}\n\n"
			f"Current User Question:\n{current_query}"
		)

	def _get_previous_user_messages(
		self,
		history: ConversationHistory,
		max_previous_messages: int,
	) -> list[str]:
		user_messages = [
			message.content
			for message in history.messages
			if message.role == ChatRole.USER
		]

		if len(user_messages) <= 1:
			return []

		previous_user_messages = user_messages[:-1]
		return previous_user_messages[-max_previous_messages:]