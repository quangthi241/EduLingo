"use client";

import { useState } from "react";

import { Button } from "@shared/ui/Button";
import { Textarea } from "@shared/ui/Textarea";
import { RubricView } from "../RubricView";
import { PieceMetaFields, type PieceMeta } from "./PieceMetaFields";

type WritingFormValue = {
  meta: PieceMeta;
  prompt: string;
  exemplar: string | null;
};

export function WritingForm({
  initial,
  onSubmit,
  submitting,
}: {
  initial?: Partial<WritingFormValue>;
  onSubmit: (v: WritingFormValue) => void;
  submitting?: boolean;
}) {
  const [value, setValue] = useState<WritingFormValue>({
    meta: initial?.meta ?? {
      slug: "",
      title: "",
      cefr: "B1",
      minutes: 10,
      topic: "business",
    },
    prompt: initial?.prompt ?? "",
    exemplar: initial?.exemplar ?? null,
  });
  return (
    <form
      className="flex flex-col gap-5"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(value);
      }}
    >
      <PieceMetaFields
        value={value.meta}
        onChange={(meta) => setValue({ ...value, meta })}
      />
      <Textarea
        label="Writing prompt"
        id="writing-prompt"
        rows={6}
        value={value.prompt}
        onChange={(e) => setValue({ ...value, prompt: e.target.value })}
      />
      <Textarea
        label="Exemplar (optional)"
        id="writing-exemplar"
        rows={8}
        value={value.exemplar ?? ""}
        onChange={(e) =>
          setValue({ ...value, exemplar: e.target.value || null })
        }
      />
      <RubricView />
      <Button type="submit" disabled={submitting}>
        Save draft
      </Button>
    </form>
  );
}
