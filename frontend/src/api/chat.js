import api from "./client";

export async function sendChatMessage({
  query,
  conversationId = null,
}) {
  return api.post("/api/v1/chat", {
    query,
    conversation_id: conversationId,
  });
}