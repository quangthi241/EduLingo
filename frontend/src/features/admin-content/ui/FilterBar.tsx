"use client";

import { Select } from "@shared/ui/Select";
import type { AdminListFilter } from "../domain/piece";

const STATUS = [
  { value: "", label: "All statuses" },
  { value: "draft", label: "Draft" },
  { value: "published", label: "Published" },
  { value: "archived", label: "Archived" },
];
const KIND = [
  { value: "", label: "All kinds" },
  { value: "reading", label: "Reading" },
  { value: "listening", label: "Listening" },
  { value: "speaking", label: "Speaking" },
  { value: "writing", label: "Writing" },
];
const CEFR = [
  { value: "", label: "All CEFR" },
  { value: "A1", label: "A1" },
  { value: "A2", label: "A2" },
  { value: "B1", label: "B1" },
  { value: "B2", label: "B2" },
  { value: "C1", label: "C1" },
];

type Props = { value: AdminListFilter; onChange: (f: AdminListFilter) => void };

export function FilterBar({ value, onChange }: Props) {
  return (
    <div className="flex flex-wrap gap-3">
      <Select
        id="filter-status"
        options={STATUS}
        value={value.status ?? ""}
        onChange={(e) =>
          onChange({
            ...value,
            status: (e.target.value || undefined) as AdminListFilter["status"],
          })
        }
      />
      <Select
        id="filter-kind"
        options={KIND}
        value={value.kind ?? ""}
        onChange={(e) =>
          onChange({
            ...value,
            kind: (e.target.value || undefined) as AdminListFilter["kind"],
          })
        }
      />
      <Select
        id="filter-cefr"
        options={CEFR}
        value={value.cefr ?? ""}
        onChange={(e) =>
          onChange({
            ...value,
            cefr: (e.target.value || undefined) as AdminListFilter["cefr"],
          })
        }
      />
    </div>
  );
}
