export default function StatusDot({
  status = "online",
}) {
  return (
    <span className={`status-dot status-${status}`}>
      <span />
    </span>
  );
}