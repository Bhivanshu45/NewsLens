import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";

export default function AppLayout() {
  const [mobileOpen, setMobileOpen] =
    useState(false);

  return (
    <div className="app-shell">
      <Sidebar
        mobileOpen={mobileOpen}
        onClose={() => setMobileOpen(false)}
      />

      <main className="main-content">
        <Outlet
          context={{
            openSidebar: () => setMobileOpen(true),
          }}
        />
      </main>
    </div>
  );
}