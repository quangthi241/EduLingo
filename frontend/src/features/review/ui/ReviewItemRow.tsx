import { ItemRow } from "@shared/ui/ItemRow";
import type { ReviewItem } from "../domain/queue";
export function ReviewItemRow({ item }: { item: ReviewItem }) {
  return (
    <ItemRow title={item.cue} meta={`due ${item.dueIn}`}>
      <span className="text-sm text-[color:var(--color-ink-subtle)]">→</span>
    </ItemRow>
  );
}
