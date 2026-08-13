import {
  Bot,
  User,
} from "lucide-react";

import ChatSource from "./ChatSource";

export default function ChatMessage({
  message,
}) {
  const isUser =
    message.role === "user";

  return (
    <div
      className={`chat-message-row ${
        isUser
          ? "chat-message-user"
          : ""
      }`}
    >
      <div
        className={`chat-avatar ${
          isUser
            ? "chat-avatar-user"
            : "chat-avatar-ai"
        }`}
      >
        {isUser ? (
          <User size={16} />
        ) : (
          <Bot size={17} />
        )}
      </div>

      <div className="chat-message-content">
        <div className="chat-message-role">
          {isUser
            ? "You"
            : "NewsLens"}
        </div>

        <div
          className={`chat-bubble ${
            message.error
              ? "chat-bubble-error"
              : ""
          }`}
        >
          {message.content
            .split("\n")
            .map((line, index) => (
              <p key={index}>
                {line ||
                  "\u00A0"}
              </p>
            ))}
        </div>

        {!isUser &&
          message.sources?.length > 0 && (
            <div className="chat-sources">
              <div className="chat-sources-heading">
                Sources
              </div>

              {message.sources.map(
                (
                  source,
                  index
                ) => (
                  <ChatSource
                    key={`${source.url}-${index}`}
                    source={source}
                    index={index}
                  />
                )
              )}
            </div>
          )}
      </div>
    </div>
  );
}