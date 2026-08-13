import {
  Bot,
  Compass,
  Home,
  Layers3,
  Newspaper,
  Search,
  X,
} from "lucide-react";

import { NavLink } from "react-router-dom";

const navigation = [
  {
    label: "Home",
    path: "/dashboard",
    icon: Home,
  },
  {
    label: "Latest News",
    path: "/articles",
    icon: Newspaper,
  },
  {
    label: "Topics",
    path: "/clusters",
    icon: Layers3,
  },
  {
    label: "Search",
    path: "/semantic-search",
    icon: Search,
  },
  {
    label: "Ask NewsLens",
    path: "/chat",
    icon: Bot,
  },
];

export default function Sidebar({
  mobileOpen,
  onClose,
}) {
  return (
    <>
      {mobileOpen && (
        <div
          className="sidebar-overlay"
          onClick={onClose}
        />
      )}

      <aside
        className={`sidebar ${
          mobileOpen ? "sidebar-open" : ""
        }`}
      >
        <div className="brand">
          <div className="brand-mark">
            <Compass size={19} />
          </div>

          <div className="brand-name">
            NewsLens
          </div>

          <button
            className="sidebar-close"
            onClick={onClose}
          >
            <X size={18} />
          </button>
        </div>

        <div className="nav-section">
          <span className="nav-section-label">
            EXPLORE
          </span>

          <nav>
            {navigation.map((item) => {
              const Icon = item.icon;

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={onClose}
                  className={({ isActive }) =>
                    `nav-item ${
                      isActive
                        ? "nav-item-active"
                        : ""
                    }`
                  }
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        <div className="sidebar-bottom">
          <div className="sidebar-ai-card">
            <Bot size={17} />

            <div>
              <strong>Have a question?</strong>

              <span>
                Ask NewsLens about the latest news.
              </span>
            </div>
          </div>

          <div className="sidebar-footer">
            NewsLens
          </div>
        </div>
      </aside>
    </>
  );
}