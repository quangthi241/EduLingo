import { useQuery } from "@tanstack/react-query";

import { apiFetch } from "@shared/api/client";
import type { Piece, PiecePage } from "../domain/pieces";

type LibraryFilter = {
  cefr?: string;
  kind?: string;
  topic?: string;
  cursor?: string;
  limit?: number;
};

function libraryUrl(f: LibraryFilter): string {
  const p = new URLSearchParams();
  if (f.cefr) p.set("cefr", f.cefr);
  if (f.kind) p.set("kind", f.kind);
  if (f.topic) p.set("topic", f.topic);
  if (f.cursor) p.set("cursor", f.cursor);
  if (f.limit) p.set("limit", String(f.limit));
  const qs = p.toString();
  return qs ? `/api/library?${qs}` : "/api/library";
}

export function useLibraryQuery(filter: LibraryFilter = {}) {
  return useQuery<PiecePage>({
    queryKey: ["library", filter],
    queryFn: () => apiFetch<PiecePage>(libraryUrl(filter)),
  });
}

export function useLibraryPieceQuery(slug: string) {
  return useQuery<Piece>({
    queryKey: ["library", "piece", slug],
    queryFn: () => apiFetch<Piece>(`/api/library/${slug}`),
  });
}
