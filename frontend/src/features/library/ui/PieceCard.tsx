import Link from "next/link";
import type { Piece } from "../domain/pieces";

export function PieceCard({ piece }: { piece: Piece }) {
  return (
    <Link
      href={`/library/${piece.slug}`}
      className="group grid grid-cols-[1fr,auto] items-baseline gap-x-6 gap-y-1 border-b border-[color:var(--color-rule)] py-5 last:border-b-0"
    >
      <div className="flex min-w-0 flex-col gap-1">
        <p className="eyebrow text-[color:var(--color-ink-subtle)]">
          {piece.kind} &middot; {piece.topic.replace("-", " ")}
        </p>
        <h3 className="font-display text-xl font-semibold leading-snug tracking-tight text-[color:var(--color-ink)] transition-colors duration-150 [transition-timing-function:var(--ease-out-quart)] group-hover:text-[color:var(--color-accent)]">
          {piece.title}
        </h3>
      </div>
      <span className="caption tabular whitespace-nowrap text-[color:var(--color-ink-subtle)] group-hover:text-[color:var(--color-ink-muted)]">
        {piece.minutes} min &middot; {piece.cefr}
      </span>
    </Link>
  );
}
