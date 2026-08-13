import {
  Layers3,
  Newspaper,
  Radio,
} from "lucide-react";

function StatCard({
  icon: Icon,
  label,
  value,
}) {
  return (
    <div className="stat-card">
      <div className="stat-icon">
        <Icon size={17} />
      </div>

      <div className="stat-content">
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

export default function IntelligenceStats({
  articles = [],
  clusters = [],
}) {
  const sources = new Set(
    articles
      .map((article) => article.source)
      .filter(Boolean)
  );

  return (
    <div className="stats-grid">
      <StatCard
        icon={Newspaper}
        label="Stories today"
        value={articles.length}
      />

      <StatCard
        icon={Layers3}
        label="Trending topics"
        value={clusters.length}
      />

      <StatCard
        icon={Radio}
        label="News sources"
        value={sources.size}
      />
    </div>
  );
}