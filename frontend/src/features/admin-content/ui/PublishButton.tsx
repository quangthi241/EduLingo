"use client";

import { useArchivePieceMutation, usePublishPieceMutation } from "../api/client";
import { Button } from "@shared/ui/Button";
import type { Piece } from "@features/library/domain/pieces";

export function PublishButton({ piece }: { piece: Piece }) {
  const pub = usePublishPieceMutation();
  const arch = useArchivePieceMutation();

  if (piece.status === "draft") {
    return (
      <Button onClick={() => pub.mutate(piece.id)} disabled={pub.isPending}>
        Publish
      </Button>
    );
  }
  if (piece.status === "published") {
    return (
      <Button
        variant="ghost"
        onClick={() => arch.mutate(piece.id)}
        disabled={arch.isPending}
      >
        Archive
      </Button>
    );
  }
  return null;
}
