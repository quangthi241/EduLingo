"use client";

import { useParams, useRouter } from "next/navigation";

import {
  useAdminPieceQuery,
  useDeletePieceMutation,
  useUpdatePieceMutation,
  useUploadMediaMutation,
} from "@features/admin-content/api/client";
import { AudioUploader } from "@features/admin-content/ui/AudioUploader";
import { PublishButton } from "@features/admin-content/ui/PublishButton";
import { StatusChip } from "@features/admin-content/ui/StatusChip";
import { Button } from "@shared/ui/Button";

export default function Page() {
  const params = useParams<{ id: string }>();
  const id = params.id;
  const router = useRouter();

  const q = useAdminPieceQuery(id);
  const update = useUpdatePieceMutation(id);
  const del = useDeletePieceMutation();
  const upload = useUploadMediaMutation(id);

  if (q.isLoading) return <p className="text-sm text-ink-muted">Loading …</p>;
  if (q.isError || !q.data)
    return <p className="text-sm text-danger">Not found.</p>;

  const piece = q.data;

  return (
    <section className="flex flex-col gap-5">
      <header className="flex items-center justify-between gap-3">
        <div>
          <h1 className="text-xl font-semibold">{piece.title}</h1>
          <p className="text-xs text-ink-muted">
            {piece.kind} • {piece.cefr} • {piece.topic}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <StatusChip
            status={piece.status as "draft" | "published" | "archived"}
          />
          <PublishButton piece={piece} />
          {piece.status === "draft" && (
            <Button
              variant="ghost"
              onClick={async () => {
                await del.mutateAsync(piece.id);
                router.push("/admin/content");
              }}
            >
              Delete
            </Button>
          )}
        </div>
      </header>

      {piece.body.kind === "listening" && (
        <section className="rounded-xl border border-border p-4">
          <h2 className="text-sm font-medium">Audio</h2>
          {piece.body.audioUrl && (
            <audio
              controls
              src={piece.body.audioUrl}
              className="mt-2 w-full"
              aria-label={`${piece.title} audio`}
            />
          )}
          <div className="mt-3">
            <AudioUploader
              uploading={upload.isPending}
              onUpload={(file) => upload.mutate(file)}
            />
          </div>
        </section>
      )}

      <section>
        <h2 className="text-sm font-medium">Inline edit</h2>
        <p className="mt-1 text-xs text-ink-muted">
          Re-upload the piece body via the form below.
        </p>
        <form
          className="mt-3 flex flex-col gap-3"
          onSubmit={(e) => {
            e.preventDefault();
            const data = new FormData(e.currentTarget);
            update.mutate({
              title: String(data.get("title") ?? piece.title),
            });
          }}
        >
          <label className="text-sm">
            Title
            <input
              name="title"
              defaultValue={piece.title}
              className="mt-1 w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm"
              disabled={piece.status !== "draft"}
            />
          </label>
          <Button
            type="submit"
            disabled={piece.status !== "draft" || update.isPending}
          >
            Save
          </Button>
        </form>
      </section>
    </section>
  );
}
