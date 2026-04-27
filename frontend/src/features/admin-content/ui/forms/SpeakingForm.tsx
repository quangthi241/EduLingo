"use client";

import { useState } from "react";

import { Button } from "@shared/ui/Button";
import { Textarea } from "@shared/ui/Textarea";
import { RubricView } from "../RubricView";
import { PieceMetaFields, type PieceMeta } from "./PieceMetaFields";

type SpeakingFormValue = { meta: PieceMeta; prompt: string };

export function SpeakingForm({
  initial,
  onSubmit,
  submitting,
}: {
  initial?: Partial<SpeakingFormValue>;
  onSubmit: (v: SpeakingFormValue) => void;
  submitting?: boolean;
}) {
  const [value, setValue] = useState<SpeakingFormValue>({
    meta: initial?.meta ?? {
      slug: "",
      title: "",
      cefr: "B1",
      minutes: 3,
      topic: "daily-life",
    },
    prompt: initial?.prompt ?? "",
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
        label="Speaking prompt"
        id="speaking-prompt"
        rows={6}
        value={value.prompt}
        onChange={(e) => setValue({ ...value, prompt: e.target.value })}
      />
      <RubricView />
      <Button type="submit" disabled={submitting}>
        Save draft
      </Button>
    </form>
  );
}
