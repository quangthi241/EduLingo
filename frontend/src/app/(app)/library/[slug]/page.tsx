import { headers } from "next/headers";
import { notFound, redirect } from "next/navigation";
import { apiBaseUrl } from "@shared/api/client";
import { ApiError } from "@shared/api/errors";
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
    const cookie = (await headers()).get("cookie") ?? "";
    const res = await fetch(`${apiBaseUrl()}/api/library/${slug}`, {
      headers: cookie ? { cookie } : {},
      cache: "no-store",
    });
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as {
        title?: string;
        detail?: string;
      };
      throw new ApiError(
        body.title ?? "error",
        body.detail ?? res.statusText,
        res.status,
      );
    }
    piece = (await res.json()) as Piece;
  } catch (err) {
    if (err instanceof ApiError) {
      console.error(
        `[library/[slug]] slug=${slug} status=${err.status} title=${err.title} detail=${err.detail}`,
      );
      if (err.status === 404) {
        notFound();
      }
      if (err.status === 401 || err.status === 403) {
        redirect("/login");
      }
    }
    throw err;
  }
  return <PiecePage piece={piece!} />;
}
