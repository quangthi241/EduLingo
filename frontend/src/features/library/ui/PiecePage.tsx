import Link from "next/link";
import type { Piece } from "../domain/pieces";

function BodyContent({ body }: { body: Piece["body"] }) {
  if (body.kind === "reading") {
    return (
      <div className="prose-editorial">
        {body.text.split(/\n\n+/).map((para, i) => (
          <p key={i}>{para}</p>
        ))}
      </div>
    );
  }
  if (body.kind === "listening") {
    return (
      <div className="prose-editorial">
        <p className="caption not-italic text-[color:var(--color-ink-subtle)]">
          Transcript
        </p>
        {body.transcript.split(/\n\n+/).map((para, i) => (
          <p key={i}>{para}</p>
        ))}
      </div>
    );
  }
  return (
    <div className="prose-editorial">
      <p>{body.prompt}</p>
    </div>
  );
}

const DATE_FMT = new Intl.DateTimeFormat("en", {
  day: "numeric",
  month: "long",
  year: "numeric",
});

export function PiecePage({ piece }: { piece: Piece }) {
  const published = piece.publishedAt
    ? DATE_FMT.format(new Date(piece.publishedAt))
    : null;

  return (
    <article className="mx-auto flex max-w-[68ch] flex-col gap-8">
      <Link
        href="/library"
        className="inline-flex items-center gap-1.5 self-start text-sm text-[color:var(--color-ink-subtle)] transition-colors hover:text-[color:var(--color-ink)]"
      >
        <span aria-hidden>&larr;</span> Library
      </Link>

      <header className="flex flex-col gap-4 border-b border-[color:var(--color-border-strong)] pb-8">
        <p className="eyebrow">
          {piece.kind} &middot; {piece.topic.replace("-", " ")}
        </p>
        <h1 className="display-2xl text-[color:var(--color-ink)]">
          {piece.title}
        </h1>
        <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 pt-1">
          <span className="dateline">
            {published ?? "Unpublished"}
          </span>
          <span className="text-[color:var(--color-ink-faint)]">&middot;</span>
          <span className="caption tabular">
            {piece.minutes} min &middot; {piece.cefr}
          </span>
          {piece.source === "llm_generated" ? (
            <span className="caption text-[color:var(--color-ink-subtle)]">
              &middot; editorial-generated
            </span>
          ) : null}
        </div>
      </header>

      {piece.body.kind === "listening" && piece.body.audioUrl && (
        <audio
          controls
          src={piece.body.audioUrl}
          className="w-full"
          preload="metadata"
          aria-label={`${piece.title} audio`}
        />
      )}

      <BodyContent body={piece.body} />

      <footer className="flex flex-col gap-3 border-t border-[color:var(--color-rule)] pt-6">
        <p className="caption">
          Finished reading? Work through it as a graded exercise and add
          anything new to your review deck.
        </p>
        <Link
          href={`/session/library-${piece.slug}`}
          className="inline-flex w-fit items-center rounded-full bg-[color:var(--color-accent)] px-5 py-2.5 text-sm font-medium text-[color:var(--color-accent-ink)] transition hover:brightness-95"
        >
          Start as exercise
        </Link>
      </footer>
    </article>
  );
}
