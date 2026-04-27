import type { InputHTMLAttributes, LabelHTMLAttributes, ReactNode } from "react";

export function Field({ children }: { children: ReactNode }) {
  return <div className="flex flex-col gap-1.5">{children}</div>;
}

export function Label({
  children,
  className = "",
  ...rest
}: LabelHTMLAttributes<HTMLLabelElement>) {
  return (
    <label
      {...rest}
      className={`text-sm font-medium text-[color:var(--color-ink-muted)] ${className}`}
    >
      {children}
    </label>
  );
}

export function Input({
  className = "",
  ...rest
}: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...rest}
      className={`rounded-md border border-[color:var(--color-border)] bg-[color:var(--color-surface)] px-3 py-2 text-base text-[color:var(--color-ink)] placeholder:text-[color:var(--color-ink-subtle)] focus-visible:border-[color:var(--color-accent)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--color-focus)] ${className}`}
    />
  );
}

export function FieldError({ children }: { children: ReactNode }) {
  return (
    <p role="alert" className="text-sm text-[color:var(--color-danger)]">
      {children}
    </p>
  );
}
