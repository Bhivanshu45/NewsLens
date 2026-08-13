import {
  ExternalLink,
} from "lucide-react";

export default function ChatSource({
  source,
  index,
}) {
  return (
    <a
      href={source.url}
      target="_blank"
      rel="noreferrer"
      className="chat-source"
    >
      <span className="chat-source-index">
        {index + 1}
      </span>

      <div className="chat-source-content">
        <strong>
          {source.title}
        </strong>

        <span>
          {source.source}
        </span>
      </div>

      <ExternalLink size={14} />
    </a>
  );
}