import { Chip, type ChipTone } from "@/shared/ui/Chip";

type Props = { status: "draft" | "published" | "archived" };

const TONE: Record<Props["status"], ChipTone> = {
  draft: "info",
  published: "success",
  archived: "neutral",
};

const LABEL: Record<Props["status"], string> = {
  draft: "Draft",
  published: "Published",
  archived: "Archived",
};

export function StatusChip({ status }: Props) {
  return <Chip tone={TONE[status]}>{LABEL[status]}</Chip>;
}
