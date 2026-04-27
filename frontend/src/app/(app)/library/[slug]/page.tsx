import { notFound } from "next/navigation";
import { apiFetch } from "@shared/api/client";
import type { Piece } from "@features/library/domain/pieces";
import { PiecePage } from "@features/library/ui/PiecePage";

export default async function LibraryPiecePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  let piece: Piece;
  try {
    piece = await apiFetch<Piece>(`/api/library/${slug}`);
  } catch {
    notFound();
  }
  return <PiecePage piece={piece!} />;
}
