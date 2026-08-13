import {
  ArrowUp,
} from "lucide-react";

import {
  useState,
} from "react";

export default function ChatInput({
  onSend,
  loading,
}) {
  const [value, setValue] =
    useState("");

  function submit(event) {
    event.preventDefault();

    if (
      !value.trim() ||
      loading
    ) {
      return;
    }

    onSend(value.trim());
    setValue("");
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      submit(event);
    }
  }

  return (
    <form
      className="chat-input-wrapper"
      onSubmit={submit}
    >
      <textarea
        value={value}
        onChange={(event) =>
          setValue(
            event.target.value
          )
        }
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about the news..."
        rows={1}
        disabled={loading}
      />

      <button
        className="chat-send"
        type="submit"
        disabled={
          !value.trim() ||
          loading
        }
      >
        <ArrowUp size={18} />
      </button>
    </form>
  );
}