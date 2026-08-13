import {
  Bot,
  RotateCcw,
} from "lucide-react";

import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

const suggestions = [
  "What are the biggest stories right now?",
  "Summarize the most important recent news.",
  "What topics are getting the most attention?",
];

export default function ChatWindow({
  messages,
  loading,
  onSend,
  onReset,
}) {
  return (
    <div className="chat-window">
      <div className="chat-window-header">
        <div className="chat-agent">
          <div className="chat-agent-icon">
            <Bot size={18} />
          </div>

          <div>
            <strong>
              Ask NewsLens
            </strong>

            <span>
              Your AI news assistant
            </span>
          </div>
        </div>

        <button
          className="new-chat-button"
          onClick={onReset}
        >
          <RotateCcw size={14} />
          New chat
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">
              <Bot size={25} />
            </div>

            <h2>
              What do you want to know?
            </h2>

            <p>
              Ask about recent stories, events,
              developments or anything covered in the
              NewsLens news feed.
            </p>

            <div className="suggestion-grid">
              {suggestions.map(
                (suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() =>
                      onSend(
                        suggestion
                      )
                    }
                  >
                    {suggestion}
                  </button>
                )
              )}
            </div>
          </div>
        ) : (
          <>
            {messages.map(
              (message) => (
                <ChatMessage
                  key={message.id}
                  message={message}
                />
              )
            )}

            {loading && (
              <div className="chat-message-row">
                <div className="chat-avatar chat-avatar-ai">
                  <Bot size={17} />
                </div>

                <div className="chat-message-content">
                  <div className="chat-message-role">
                    NewsLens
                  </div>

                  <div className="chat-thinking">
                    <span />
                    <span />
                    <span />
                    <em>
                      Thinking...
                    </em>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      <div className="chat-composer">
        <ChatInput
          onSend={onSend}
          loading={loading}
        />

        <p>
          NewsLens answers using the stories in its
          news collection.
        </p>
      </div>
    </div>
  );
}