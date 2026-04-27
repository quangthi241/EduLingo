"use client";

import Link from "next/link";

const KINDS: Array<{
  kind: "reading" | "listening" | "speaking" | "writing";
  label: string;
  hint: string;
}> = [
  { kind: "reading", label: "Reading", hint: "Passage + MCQ + short answer" },
  {
    kind: "listening",
    label: "Listening",
    hint: "Transcript + MCQ (audio uploaded after)",
  },
  { kind: "speaking", label: "Speaking", hint: "Scenario prompt + rubric" },
  { kind: "writing", label: "Writing", hint: "Task prompt + optional exemplar" },
];

export function KindPicker() {
  return (
    <ul className="grid gap-3 md:grid-cols-2">
      {KINDS.map((k) => (
        <li key={k.kind}>
          <Link
            href={`/admin/content/new?kind=${k.kind}`}
            className="block rounded-xl border border-border p-4 hover:bg-surface"
          >
            <p className="font-medium">{k.label}</p>
            <p className="text-sm text-ink-muted">{k.hint}</p>
          </Link>
        </li>
      ))}
    </ul>
  );
}
