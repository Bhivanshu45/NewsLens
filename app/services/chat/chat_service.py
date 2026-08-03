from app.services.chat.context_builder import ContextBuilder
from app.services.chat.conversation_service import ConversationService
from app.services.chat.retrieval_query_builder import RetrievalQueryBuilder
from app.services.chat.schemas import ChatRequest
from app.services.chat.schemas import ChatResponse
from app.services.chat.schemas import SourceReference
from app.core.constants import MAX_RETRIEVAL_HISTORY
from app.services.llm.groq_service import GroqService
from app.services.retrieval.retrieval_service import RetrievalService
from app.services.retrieval.schemas import RetrievedArticle


class ChatService:

	def __init__(
		self,
		conversation_service: ConversationService,
		retrieval_service: RetrievalService,
		retrieval_query_builder: RetrievalQueryBuilder,
		context_builder: ContextBuilder,
		groq_service: GroqService,
	):
		self.conversation_service = conversation_service
		self.retrieval_service = retrieval_service
		self.retrieval_query_builder = retrieval_query_builder
		self.context_builder = context_builder
		self.groq_service = groq_service

	def chat(
		self,
		request: ChatRequest,
	) -> ChatResponse:
		conversation_id = self._get_or_create_conversation_id(
			request.conversation_id,
		)

		self.conversation_service.append_user_message(
			conversation_id=conversation_id,
			content=request.query,
		)

		history = self.conversation_service.get_history(
			conversation_id,
		)

		retrieval_query = self.retrieval_query_builder.build(
			history=history,
			current_query=request.query,
			max_previous_messages=MAX_RETRIEVAL_HISTORY,
		)

		retrieved_articles = self.retrieval_service.retrieve(
			query=retrieval_query,
			limit=3,
		)

		prompt = self.context_builder.build_context(
			history=history,
			retrieved_articles=retrieved_articles,
		)

		answer = self.groq_service.generate_chat_completion(
			prompt,
		)

		self.conversation_service.append_assistant_message(
			conversation_id=conversation_id,
			content=answer,
		)

		return ChatResponse(
			conversation_id=conversation_id,
			answer=answer,
			sources=self._build_sources(retrieved_articles),
		)

	def _get_or_create_conversation_id(
		self,
		conversation_id: str | None,
	) -> str:
		if conversation_id is None:
			return self.conversation_service.create_conversation()

		return conversation_id

	def _build_sources(
		self,
		retrieved_articles: list[RetrievedArticle],
	) -> list[SourceReference]:
		return [
			SourceReference(
				title=retrieved_article.article.title,
				source=retrieved_article.article.source,
				url=retrieved_article.article.url,
			)
			for retrieved_article in retrieved_articles
		]
