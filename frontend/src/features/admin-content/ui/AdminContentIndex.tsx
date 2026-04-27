"use client";

import Link from "next/link";
import { useState } from "react";

import { useAdminPiecesQuery } from "../api/client";
import type { AdminListFilter } from "../domain/piece";
import { AdminContentRow } from "./AdminContentRow";
import { FilterBar } from "./FilterBar";

const PRIMARY_LINK =
  "inline-flex items-center justify-center gap-2 rounded-full font-medium transition px-4 py-2 text-base bg-[color:var(--color-accent)] text-[color:var(--color-accent-ink)] hover:brightness-95";
const GHOST_LINK =
  "inline-flex items-center justify-center gap-2 rounded-full font-medium transition px-4 py-2 text-base border border-[color:var(--color-border)] bg-transparent text-[color:var(--color-ink)] hover:bg-[color:var(--color-surface-sunken)]";

export function AdminContentIndex() {
  const [filter, setFilter] = useState<AdminListFilter>({});
  const q = useAdminPiecesQuery(filter);

  return (
    <section className="flex flex-col gap-5">
      <header className="flex items-center justify-between gap-3">
        <h1 className="text-xl font-semibold">Content</h1>
        <div className="flex gap-2">
          <Link href="/admin/content/generate" className={GHOST_LINK}>
            Generate draft
          </Link>
          <Link href="/admin/content/new" className={PRIMARY_LINK}>
            New piece
          </Link>
        </div>
      </header>
      <FilterBar value={filter} onChange={setFilter} />
      {q.isLoading && <p className="text-sm text-ink-muted">Loading …</p>}
      {q.isError && (
        <p className="text-sm text-danger">Could not load content.</p>
      )}
      {q.data && (
        <ul className="flex flex-col gap-2">
          {q.data.items.map((p) => (
            <AdminContentRow key={p.id} piece={p} />
          ))}
          {q.data.items.length === 0 && (
            <li className="text-sm text-ink-muted">No pieces match.</li>
          )}
        </ul>
      )}
    </section>
  );
}
