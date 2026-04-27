"use client";

import { useRouter, useSearchParams } from "next/navigation";

import { useCreatePieceMutation } from "@features/admin-content/api/client";
import { KindPicker } from "@features/admin-content/ui/KindPicker";
import { ListeningForm } from "@features/admin-content/ui/forms/ListeningForm";
import { ReadingForm } from "@features/admin-content/ui/forms/ReadingForm";
import { SpeakingForm } from "@features/admin-content/ui/forms/SpeakingForm";
import { WritingForm } from "@features/admin-content/ui/forms/WritingForm";
import { type PieceMeta } from "@features/admin-content/ui/forms/PieceMetaFields";

type Kind = "reading" | "listening" | "speaking" | "writing";

export function NewContentClient() {
  const params = useSearchParams();
  const kind = params.get("kind") as Kind | null;
  const router = useRouter();
  const create = useCreatePieceMutation();

  if (!kind) return <KindPicker />;

  async function save(body: object, meta: PieceMeta) {
    const piece = await create.mutateAsync({
      kind: kind!,
      slug: meta.slug,
      title: meta.title,
      cefr: meta.cefr,
      minutes: meta.minutes,
      topic: meta.topic,
      body: { kind: kind!, ...body },
    });
    router.push(`/admin/content/${piece.id}`);
  }

  if (kind === "reading") {
    return (
      <ReadingForm
        onSubmit={(v) =>
          save({ text: v.text, mcq: v.mcq, shortAnswer: v.shortAnswer }, v.meta)
        }
        submitting={create.isPending}
      />
    );
  }
  if (kind === "listening") {
    return (
      <ListeningForm
        onSubmit={(v) =>
          save(
            {
              audioRef: null,
              transcript: v.transcript,
              mcq: v.mcq,
              shortAnswer: v.shortAnswer,
            },
            v.meta,
          )
        }
        submitting={create.isPending}
      />
    );
  }
  if (kind === "speaking") {
    return (
      <SpeakingForm
        onSubmit={(v) =>
          save({ prompt: v.prompt, referenceAudioRef: null }, v.meta)
        }
        submitting={create.isPending}
      />
    );
  }
  if (kind === "writing") {
    return (
      <WritingForm
        onSubmit={(v) =>
          save({ prompt: v.prompt, exemplar: v.exemplar }, v.meta)
        }
        submitting={create.isPending}
      />
    );
  }
  return <KindPicker />;
}
