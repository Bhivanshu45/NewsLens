import { Inbox } from "lucide-react";

export default function EmptyState({
  title = "Nothing here yet",
  description = "There is no data available to display.",
  icon: Icon = Inbox,
}) {
  return (
    <div className="empty-state">
      <div className="empty-state-icon">
        <Icon size={22} />
      </div>

      <h3>{title}</h3>

      <p>{description}</p>
    </div>
  );
}