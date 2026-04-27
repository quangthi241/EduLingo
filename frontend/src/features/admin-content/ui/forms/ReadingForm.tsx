"use client";

import { useState } from "react";

import { Button } from "@shared/ui/Button";
import { Field, Label, Input } from "@shared/ui/Field";
import { Textarea } from "@shared/ui/Textarea";
import type { MCQ } from "@features/library/domain/pieces";
import { MCQBuilder } from "../MCQBuilder";
import { PieceMetaFields, type PieceMeta } from "./PieceMetaFields";

type ReadingFormValue = {
  meta: PieceMeta;
  text: string;
  mcq: MCQ[];
  shortAnswer: { prompt: string; gradingNotes: string };
};

export function ReadingForm({
  initial,
  onSubmit,
  submitting,
}: {
  initial?: Partial<ReadingFormValue>;
  onSubmit: (value: ReadingFormValue) => void;
  submitting?: boolean;
}) {
  const [value, setValue] = useState<ReadingFormValue>({
    meta: initial?.meta ?? {
      slug: "",
      title: "",
      cefr: "B1",
      minutes: 5,
      topic: "travel",
    },
    text: initial?.text ?? "",
    mcq:
      initial?.mcq ??
      Array.from({ length: 3 }, () => ({
        question: "",
        choices: ["", ""],
        correctIndex: 0,
        rationale: "",
      })),
    shortAnswer: initial?.shortAnswer ?? { prompt: "", gradingNotes: "" },
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
        label="Passage"
        id="reading-text"
        rows={10}
        value={value.text}
        onChange={(e) => setValue({ ...value, text: e.target.value })}
      />
      <MCQBuilder
        value={value.mcq}
        onChange={(mcq) => setValue({ ...value, mcq })}
      />
      <fieldset className="rounded-xl border border-border p-4 flex flex-col gap-3">
        <legend className="px-1 text-sm text-ink-muted">Short answer</legend>
        <Field>
          <Label htmlFor="sa-prompt">Prompt</Label>
          <Input
            id="sa-prompt"
            value={value.shortAnswer.prompt}
            onChange={(e) =>
              setValue({
                ...value,
                shortAnswer: { ...value.shortAnswer, prompt: e.target.value },
              })
            }
          />
        </Field>
        <Textarea
          label="Grading notes"
          id="sa-notes"
          rows={2}
          value={value.shortAnswer.gradingNotes}
          onChange={(e) =>
            setValue({
              ...value,
              shortAnswer: {
                ...value.shortAnswer,
                gradingNotes: e.target.value,
              },
            })
          }
        />
      </fieldset>
      <Button type="submit" disabled={submitting}>
        Save draft
      </Button>
    </form>
  );
}
