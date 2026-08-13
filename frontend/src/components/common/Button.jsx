import { LoaderCircle } from "lucide-react";

export default function Button({
  children,
  loading = false,
  variant = "primary",
  size = "md",
  className = "",
  disabled,
  ...props
}) {
  return (
    <button
      className={`button button-${variant} button-${size} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <LoaderCircle
          size={16}
          className="spin"
        />
      )}

      {children}
    </button>
  );
}