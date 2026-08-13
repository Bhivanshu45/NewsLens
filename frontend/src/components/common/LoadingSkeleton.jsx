export function Skeleton({
  className = "",
}) {
  return (
    <div
      className={`skeleton ${className}`}
    />
  );
}

export function CardSkeleton() {
  return (
    <div className="article-card skeleton-card">
      <Skeleton className="skeleton-line small" />
      <Skeleton className="skeleton-line title" />
      <Skeleton className="skeleton-line title short" />
      <Skeleton className="skeleton-line body" />
      <Skeleton className="skeleton-line body short" />

      <div className="skeleton-footer">
        <Skeleton className="skeleton-circle" />
        <Skeleton className="skeleton-line small" />
      </div>
    </div>
  );
}

export function GridSkeleton({
  count = 6,
}) {
  return (
    <div className="article-grid">
      {Array.from({ length: count }).map((_, index) => (
        <CardSkeleton key={index} />
      ))}
    </div>
  );
}