"use client";

import Link from "next/link";

import type { Piece } from "@features/library/domain/pieces";
import { StatusChip } from "./StatusChip";

export function AdminContentRow({ piece }: { piece: Piece }) {
  return (
    <li className="flex items-center justify-between gap-4 rounded-xl border border-border px-4 py-3">
      <div className="min-w-0">
        <p className="truncate font-medium">{piece.title}</p>
        <p className="text-xs text-ink-muted">
          {piece.kind} • {piece.cefr} • {piece.topic}
        </p>
      </div>
      <div className="flex items-center gap-3">
        <StatusChip status={piece.status as "draft" | "published" | "archived"} />
        <Link
          href={`/admin/content/${piece.id}`}
          className="text-sm text-accent hover:underline"
        >
          Edit
        </Link>
      </div>
    </li>
  );
}
