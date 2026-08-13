import {
  CardSkeleton,
  GridSkeleton,
  Skeleton,
} from "../common/LoadingSkeleton";

export function ArticleDetailSkeleton() {
  return (
    <div className="article-detail">
      <Skeleton className="skeleton-line small" />
      <Skeleton className="skeleton-line hero-title" />
      <Skeleton className="skeleton-line hero-title short" />

      <div className="detail-meta-skeleton">
        <Skeleton className="skeleton-circle" />
        <Skeleton className="skeleton-line small" />
      </div>

      <Skeleton className="detail-block" />
      <Skeleton className="detail-block" />
      <Skeleton className="detail-block short" />
    </div>
  );
}

export { CardSkeleton, GridSkeleton };