import type { ButtonHTMLAttributes, ReactNode } from "react";

type Variant = "primary" | "ghost" | "text" | "quiet";
type Size = "sm" | "md" | "lg";

const VARIANTS: Record<Variant, string> = {
  primary:
    "bg-[color:var(--color-accent)] text-[color:var(--color-accent-ink)] hover:brightness-95 disabled:opacity-50",
  ghost:
    "border border-[color:var(--color-border-strong)] bg-transparent text-[color:var(--color-ink)] hover:border-[color:var(--color-ink)] hover:bg-[color:var(--color-surface-sunken)]",
  text: "bg-transparent text-[color:var(--color-accent)] hover:underline underline-offset-4",
  quiet:
    "bg-[color:var(--color-surface-sunken)] text-[color:var(--color-ink)] hover:bg-[color:var(--color-surface-raised)]",
};

const SIZES: Record<Size, string> = {
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-base",
  lg: "px-6 py-3 text-base",
};

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  loading?: boolean;
  children: ReactNode;
}

export function Button({
  variant = "primary",
  size = "md",
  loading = false,
  disabled,
  children,
  className = "",
  ...rest
}: ButtonProps) {
  return (
    <button
      {...rest}
      data-variant={variant}
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center gap-2 rounded-full font-medium transition-[background-color,border-color,color,transform] duration-200 [transition-timing-function:var(--ease-out-quart)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[color:var(--color-accent)] active:translate-y-[0.5px] ${VARIANTS[variant]} ${SIZES[size]} ${className}`}
    >
      {loading ? <span aria-hidden>…</span> : children}
    </button>
  );
}
