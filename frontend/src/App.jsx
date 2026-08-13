import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'

import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import Dashboard from "./pages/Dashboard";
import Articles from "./pages/Articles";
import ArticlePage from "./pages/ArticlePage";
import Clusters from "./pages/Clusters";
import ClusterPage from "./pages/ClusterPage";
import SemanticSearch from "./pages/SemanticSearch";
import Chat from "./pages/Chat";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/articles" element={<Articles />} />
        <Route path="/articles/:articleId" element={<ArticlePage />} />

        <Route path="/clusters" element={<Clusters />} />
        <Route path="/clusters/:clusterId" element={<ClusterPage />} />

        <Route path="/semantic-search" element={<SemanticSearch />} />

        <Route path="/chat" element={<Chat />} />

        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
