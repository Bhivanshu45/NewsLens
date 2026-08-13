import {
  Bot,
  Newspaper,
} from "lucide-react";

import {
  useOutletContext,
} from "react-router-dom";

import Header from "../components/layout/Header";
import ChatWindow from "../components/chat/ChatWindow";

import {
  useChat,
} from "../hooks/useChat";

export default function Chat() {
  const { openSidebar } =
    useOutletContext() || {};

  const {
    messages,
    loading,
    sendMessage,
    resetConversation,
  } = useChat();

  return (
    <>
      <Header
        title="Ask NewsLens"
        subtitle="Have a question about the news?"
        onMenuClick={openSidebar}
      />

      <div className="page-content chat-page">
        <div className="chat-layout">
          <aside className="chat-info-panel">
            <div className="chat-info-icon">
              <Bot size={21} />
            </div>

            <span className="eyebrow">
              YOUR NEWS ASSISTANT
            </span>

            <h2>
              Ask about what's happening.
            </h2>

            <p>
              Ask questions about recent stories,
              events and topics covered by NewsLens.
            </p>

            <div className="chat-info-note">
              <Newspaper size={17} />

              <span>
                Answers include links to the stories
                they are based on, so you can always
                read the original coverage.
              </span>
            </div>
          </aside>

          <ChatWindow
            messages={messages}
            loading={loading}
            onSend={sendMessage}
            onReset={resetConversation}
          />
        </div>
      </div>
    </>
  );
}