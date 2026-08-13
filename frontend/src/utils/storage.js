const CONVERSATION_KEY = "newslens_conversation_id";

export function getConversationId() {
  return localStorage.getItem(CONVERSATION_KEY);
}

export function saveConversationId(id) {
  if (id) {
    localStorage.setItem(CONVERSATION_KEY, id);
  }
}

export function clearConversationId() {
  localStorage.removeItem(CONVERSATION_KEY);
}