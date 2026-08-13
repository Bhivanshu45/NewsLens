import { AlertTriangle, RotateCcw } from "lucide-react";

export default function ErrorState({
  message = "Something went wrong.",
  onRetry,
}) {
  return (
    <div className="error-state">
      <div className="error-state-icon">
        <AlertTriangle size={20} />
      </div>

      <div>
        <strong>Unable to load data</strong>
        <p>{message}</p>
      </div>

      {onRetry && (
        <button
          className="icon-button"
          onClick={onRetry}
          title="Retry"
        >
          <RotateCcw size={17} />
        </button>
      )}
    </div>
  );
}