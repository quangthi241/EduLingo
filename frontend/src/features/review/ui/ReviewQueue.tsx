"use client";

import { useMemo, useState } from "react";
import { REVIEW_ITEMS, type ReviewItem } from "../domain/queue";
import { ReviewCard } from "./ReviewCard";

type Rating = "again" | "hard" | "good" | "easy";

export function ReviewQueue() {
  const due = useMemo(() => REVIEW_ITEMS.filter((i) => i.dueIn === "now"), []);
  const [index, setIndex] = useState(0);
  const [done, setDone] = useState<{ id: string; rating: Rating }[]>([]);
  const current = due[index];

  function rate(rating: Rating) {
    if (!current) return;
    setDone((d) => [...d, { id: current.id, rating }]);
    setIndex((i) => i + 1);
  }

  return (
    <div className="mx-auto flex max-w-[72ch] flex-col gap-10">
      <header className="flex flex-col gap-3">
        <p className="eyebrow">Spaced review</p>
        <h1 className="display-xl text-[color:var(--color-ink)]">Review</h1>
        <p className="text-[color:var(--color-ink-muted)]">
          {due.length} items due today. Rate your recall honestly &mdash;
          the pathway recalibrates from the answers you give, not from
          how quickly you clear the queue.
        </p>
      </header>

      {current ? (
        <ReviewCard
          key={current.id}
          item={current}
          position={index + 1}
          total={due.length}
          onRate={rate}
        />
      ) : (
        <DoneCard count={done.length} />
      )}

      <RemainingList items={due} doneIds={done.map((d) => d.id)} />
    </div>
  );
}

function DoneCard({ count }: { count: number }) {
  return (
    <section className="surface-card flex flex-col gap-3 p-8 text-center">
      <p className="eyebrow mx-auto">Queue clear</p>
      <h2 className="display-lg">All {count} items reviewed.</h2>
      <p className="text-[color:var(--color-ink-muted)]">
        The next batch surfaces tomorrow morning. Keep the day gentle.
      </p>
    </section>
  );
}

function RemainingList({
  items,
  doneIds,
}: {
  items: ReviewItem[];
  doneIds: string[];
}) {
  const grammar = items.filter((i) => i.kind === "grammar");
  const vocab = items.filter((i) => i.kind === "vocabulary");
  return (
    <section
      aria-labelledby="today-queue"
      className="flex flex-col gap-6 border-t border-[color:var(--color-rule)] pt-8"
    >
      <h2 id="today-queue" className="eyebrow">
        Today&rsquo;s queue
      </h2>
      <div className="grid gap-8 md:grid-cols-2">
        <QueueColumn title="Grammar" items={grammar} doneIds={doneIds} />
        <QueueColumn title="Vocabulary" items={vocab} doneIds={doneIds} />
      </div>
    </section>
  );
}

function QueueColumn({
  title,
  items,
  doneIds,
}: {
  title: string;
  items: ReviewItem[];
  doneIds: string[];
}) {
  return (
    <div className="flex flex-col gap-3">
      <h3 className="font-display text-lg font-semibold tracking-tight text-[color:var(--color-ink)]">
        {title}
      </h3>
      <ul className="flex flex-col">
        {items.map((i) => {
          const done = doneIds.includes(i.id);
          return (
            <li
              key={i.id}
              className="flex items-baseline justify-between gap-3 border-b border-[color:var(--color-rule)] py-2.5 text-sm last:border-b-0"
            >
              <span
                className={
                  done
                    ? "text-[color:var(--color-ink-faint)] line-through"
                    : "text-[color:var(--color-ink)]"
                }
              >
                {i.cue}
              </span>
              <span className="caption tabular">{i.dueIn}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
