"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { Button } from "@/shared/ui/Button";
import { Select } from "@/shared/ui/Select";
import { Textarea } from "@/shared/ui/Textarea";
import { useGeneratePieceMutation } from "../api/client";
import type { GenerateInput } from "../domain/piece";
import type { Piece } from "@/features/library/domain/pieces";

const KIND = [
  { value: "reading", label: "Reading" },
  { value: "listening", label: "Listening" },
  { value: "speaking", label: "Speaking" },
  { value: "writing", label: "Writing" },
];
const CEFR = ["A1", "A2", "B1", "B2", "C1"].map((v) => ({ value: v, label: v }));
const TOPIC = [
  "travel",
  "business",
  "daily-life",
  "academic",
  "culture",
  "science",
].map((v) => ({ value: v, label: v }));

export function GenerateWizard() {
  const [spec, setSpec] = useState<GenerateInput>({
    kind: "reading",
    cefr: "B1",
    topic: "travel",
    seedPrompt: "",
  });
  const [preview, setPreview] = useState<Piece | null>(null);
  const mut = useGeneratePieceMutation();
  const router = useRouter();

  async function run() {
    const piece = await mut.mutateAsync({
      ...spec,
      seedPrompt: spec.seedPrompt || undefined,
    });
    setPreview(piece);
  }

  if (preview) {
    return (
      <section className="flex flex-col gap-4">
        <h2 className="text-lg font-semibold">{preview.title}</h2>
        <p className="text-sm text-ink-muted">
          {preview.kind} • {preview.cefr} • {preview.topic}
        </p>
        <pre className="whitespace-pre-wrap rounded-xl border border-border p-4 text-sm">
          {JSON.stringify(preview.body, null, 2)}
        </pre>
        <div className="flex gap-2">
          <Button onClick={() => router.push(`/admin/content/${preview.id}`)}>
            Save as draft
          </Button>
          <Button variant="ghost" onClick={() => setPreview(null)}>
            Regenerate
          </Button>
          <Button variant="ghost" onClick={() => setPreview(null)}>
            Discard
          </Button>
        </div>
      </section>
    );
  }

  return (
    <form
      className="flex flex-col gap-4"
      onSubmit={(e) => {
        e.preventDefault();
        run();
      }}
    >
      <Select
        label="Kind"
        id="gen-kind"
        options={KIND}
        value={spec.kind}
        onChange={(e) =>
          setSpec({ ...spec, kind: e.target.value as GenerateInput["kind"] })
        }
      />
      <Select
        label="CEFR"
        id="gen-cefr"
        options={CEFR}
        value={spec.cefr}
        onChange={(e) => setSpec({ ...spec, cefr: e.target.value })}
      />
      <Select
        label="Topic"
        id="gen-topic"
        options={TOPIC}
        value={spec.topic}
        onChange={(e) => setSpec({ ...spec, topic: e.target.value })}
      />
      <Textarea
        label="Seed prompt (optional)"
        id="gen-seed"
        rows={3}
        value={spec.seedPrompt ?? ""}
        onChange={(e) => setSpec({ ...spec, seedPrompt: e.target.value })}
      />
      <Button type="submit" disabled={mut.isPending}>
        {mut.isPending ? "Generating …" : "Generate"}
      </Button>
      {mut.isError && (
        <p role="alert" className="text-sm text-danger">
          Generation failed. Try again or adjust your prompt.
        </p>
      )}
    </form>
  );
}
