"use client";

import { Field, Label, Input } from "@shared/ui/Field";
import { Select } from "@shared/ui/Select";

export type PieceMeta = {
  slug: string;
  title: string;
  cefr: string;
  minutes: number;
  topic: string;
};

type Props = {
  value: PieceMeta;
  onChange: (v: PieceMeta) => void;
  disableSlug?: boolean;
};

const CEFR = ["A1", "A2", "B1", "B2", "C1"].map((v) => ({ value: v, label: v }));
const TOPICS = [
  "travel",
  "business",
  "daily-life",
  "academic",
  "culture",
  "science",
].map((v) => ({ value: v, label: v }));

export function PieceMetaFields({ value, onChange, disableSlug }: Props) {
  function patch<K extends keyof PieceMeta>(k: K, v: PieceMeta[K]) {
    onChange({ ...value, [k]: v });
  }
  return (
    <div className="grid gap-3 md:grid-cols-2">
      <Field>
        <Label htmlFor="meta-slug">Slug</Label>
        <Input
          id="meta-slug"
          value={value.slug}
          onChange={(e) => patch("slug", e.target.value)}
          disabled={disableSlug}
        />
      </Field>
      <Field>
        <Label htmlFor="meta-title">Title</Label>
        <Input
          id="meta-title"
          value={value.title}
          onChange={(e) => patch("title", e.target.value)}
        />
      </Field>
      <Select
        label="CEFR"
        id="meta-cefr"
        options={CEFR}
        value={value.cefr}
        onChange={(e) => patch("cefr", e.target.value)}
      />
      <Select
        label="Topic"
        id="meta-topic"
        options={TOPICS}
        value={value.topic}
        onChange={(e) => patch("topic", e.target.value)}
      />
      <Field>
        <Label htmlFor="meta-minutes">Minutes</Label>
        <Input
          id="meta-minutes"
          type="number"
          min={1}
          max={60}
          value={value.minutes}
          onChange={(e) => patch("minutes", Number(e.target.value))}
        />
      </Field>
    </div>
  );
}
