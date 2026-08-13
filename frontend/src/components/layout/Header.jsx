import {
  Menu,
  RefreshCw,
} from "lucide-react";

export default function Header({
  title,
  subtitle,
  onMenuClick,
  onRefresh,
  refreshing = false,
}) {
  return (
    <header className="header">
      <div className="header-left">
        <button
          className="mobile-menu-button"
          onClick={onMenuClick}
        >
          <Menu size={21} />
        </button>

        <div>
          <h1>{title}</h1>

          {subtitle && (
            <p>{subtitle}</p>
          )}
        </div>
      </div>

      {onRefresh && (
        <button
          className="header-refresh"
          onClick={onRefresh}
          disabled={refreshing}
        >
          <RefreshCw
            size={15}
            className={
              refreshing ? "spin" : ""
            }
          />

          <span>Refresh</span>
        </button>
      )}
    </header>
  );
}