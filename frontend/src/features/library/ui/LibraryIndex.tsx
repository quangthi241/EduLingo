"use client";

import { useLibraryQuery } from "../api/client";
import type { Piece } from "../domain/pieces";
import { PieceCard } from "./PieceCard";

export function LibraryIndex() {
  const q = useLibraryQuery();
  const items = q.data?.items ?? [];
  const [featured, ...rest] = items;

  return (
    <div className="mx-auto flex max-w-[72ch] flex-col gap-10">
      <header className="flex flex-col gap-3">
        <p className="eyebrow">Archive</p>
        <h1 className="display-xl text-[color:var(--color-ink)]">Library</h1>
        <p className="max-w-[60ch] text-[color:var(--color-ink-muted)]">
          A working collection of reading, listening, speaking and writing
          pieces. New material is added each week; nothing is tied to a
          streak. Read what you&rsquo;re drawn to.
        </p>
      </header>

      <nav
        aria-label="Filter by kind"
        className="flex flex-wrap gap-x-5 gap-y-2 border-y border-[color:var(--color-rule)] py-3"
      >
        {[
          { label: "All", href: "/library" },
          { label: "Reading", href: "/library?skill=reading" },
          { label: "Listening", href: "/library?skill=listening" },
          { label: "Speaking", href: "/library?skill=speaking" },
          { label: "Writing", href: "/library?skill=writing" },
        ].map((f, i) => (
          <a
            key={f.href}
            href={f.href}
            aria-current={i === 0 ? "page" : undefined}
            className={`text-sm transition-colors duration-150 [transition-timing-function:var(--ease-out-quart)] ${
              i === 0
                ? "text-[color:var(--color-ink)]"
                : "text-[color:var(--color-ink-muted)] hover:text-[color:var(--color-ink)]"
            }`}
          >
            {f.label}
          </a>
        ))}
      </nav>

      <Body
        q={q}
        featured={featured as Piece | undefined}
        rest={rest as Piece[]}
      />
    </div>
  );
}

function Body({
  q,
  featured,
  rest,
}: {
  q: ReturnType<typeof useLibraryQuery>;
  featured: Piece | undefined;
  rest: Piece[];
}) {
  if (q.isLoading) {
    return (
      <p className="dateline text-[color:var(--color-ink-muted)]">
        Setting the type &hellip;
      </p>
    );
  }
  if (q.isError) {
    return (
      <p className="text-sm text-[color:var(--color-danger)]">
        Could not load library. Try again.
      </p>
    );
  }
  if (!featured) {
    return (
      <div className="flex flex-col gap-3 pt-4">
        <p className="dateline text-[color:var(--color-ink-muted)]">
          Nothing on the shelf yet.
        </p>
        <p className="text-sm text-[color:var(--color-ink-subtle)]">
          New pieces publish each Monday morning. Your next one is being
          set now.
        </p>
      </div>
    );
  }
  return (
    <>
      <FeaturedPiece piece={featured} />
      {rest.length > 0 ? (
        <section aria-labelledby="more-pieces" className="flex flex-col gap-2">
          <h2 id="more-pieces" className="eyebrow pb-1">
            More in the archive
          </h2>
          <ul className="flex flex-col">
            {rest.map((piece) => (
              <li key={piece.id}>
                <PieceCard piece={piece} />
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </>
  );
}

function FeaturedPiece({ piece }: { piece: Piece }) {
  return (
    <section
      aria-labelledby="featured-piece"
      className="flex flex-col gap-4 border-b border-[color:var(--color-border-strong)] pb-10"
    >
      <div className="flex items-baseline justify-between gap-4">
        <p className="eyebrow">This week &middot; {piece.kind}</p>
        <p className="caption tabular">
          {piece.minutes} min &middot; {piece.cefr}
        </p>
      </div>
      <h2 id="featured-piece">
        <a
          href={`/library/${piece.slug}`}
          className="display-lg text-[color:var(--color-ink)] transition-colors duration-150 [transition-timing-function:var(--ease-out-quart)] hover:text-[color:var(--color-accent)]"
        >
          {piece.title}
        </a>
      </h2>
      <p className="prose-editorial max-w-[60ch] text-lg text-[color:var(--color-ink-muted)]">
        {pieceBlurb(piece)}
      </p>
      <a
        href={`/library/${piece.slug}`}
        className="mt-1 inline-flex w-fit items-center gap-1.5 text-sm font-medium text-[color:var(--color-accent)] underline-offset-4 hover:underline"
      >
        Open piece <span aria-hidden>&rarr;</span>
      </a>
    </section>
  );
}

function pieceBlurb(piece: Piece): string {
  if (piece.body.kind === "reading") {
    const preview = piece.body.text.trim().slice(0, 180);
    return preview.length < piece.body.text.trim().length
      ? `${preview}…`
      : preview;
  }
  if (piece.body.kind === "listening") {
    const preview = piece.body.transcript.trim().slice(0, 180);
    return preview.length < piece.body.transcript.trim().length
      ? `${preview}…`
      : preview;
  }
  return piece.body.prompt;
}
