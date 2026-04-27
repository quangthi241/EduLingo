import { HTMLAttributes } from "react";

export type ChipTone = "neutral" | "info" | "success" | "warning" | "danger";

const TONE_CLASSES: Record<ChipTone, string> = {
  neutral:
    "bg-[color:var(--color-surface-sunken)] text-[color:var(--color-ink-muted)] ring-1 ring-[color:var(--color-border)]",
  info: "bg-[color:var(--color-accent-quiet)] text-[color:var(--color-accent)] ring-1 ring-[color:var(--color-accent-soft)]",
  success:
    "bg-[color:var(--color-success)]/10 text-[color:var(--color-success)] ring-1 ring-[color:var(--color-success)]/30",
  warning:
    "bg-[color:var(--color-warning)]/10 text-[color:var(--color-warning)] ring-1 ring-[color:var(--color-warning)]/30",
  danger:
    "bg-[color:var(--color-danger)]/10 text-[color:var(--color-danger)] ring-1 ring-[color:var(--color-danger)]/30",
};

type Props = HTMLAttributes<HTMLSpanElement> & { tone?: ChipTone };

export function Chip({ tone = "neutral", className, ...rest }: Props) {
  const classes = [
    "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-[0.72rem] font-medium uppercase tracking-[0.08em]",
    TONE_CLASSES[tone],
    className ?? "",
  ]
    .filter(Boolean)
    .join(" ");
  return <span className={classes} {...rest} />;
}
