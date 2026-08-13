import { useCallback, useState } from "react";

import { sendChatMessage } from "../api/chat";
import {
  clearConversationId,
  getConversationId,
  saveConversationId,
} from "../utils/storage";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState(
    getConversationId()
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = useCallback(async (query) => {
    if (!query.trim() || loading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: query.trim(),
    };

    setMessages((current) => [...current, userMessage]);
    setLoading(true);
    setError("");

    try {
      const response = await sendChatMessage({
        query: query.trim(),
        conversationId,
      });

      if (response.conversation_id) {
        saveConversationId(response.conversation_id);
        setConversationId(response.conversation_id);
      }

      const assistantMessage = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.answer,
        sources: response.sources || [],
      };

      setMessages((current) => [
        ...current,
        assistantMessage,
      ]);

      return response;
    } catch (err) {
      setError(err.message || "Unable to reach NewsLens AI");

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content:
            "I couldn't process that request right now. Please try again.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }, [conversationId, loading]);

  const resetConversation = useCallback(() => {
    clearConversationId();
    setConversationId(null);
    setMessages([]);
    setError("");
  }, []);

  return {
    messages,
    conversationId,
    loading,
    error,
    sendMessage,
    resetConversation,
  };
}