import { TextareaHTMLAttributes, forwardRef } from "react";

type Props = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label?: string;
  hint?: string;
  error?: string;
};

export const Textarea = forwardRef<HTMLTextAreaElement, Props>(
  ({ label, hint, error, id, className, ...rest }, ref) => {
    const describedBy = error
      ? `${id}-error`
      : hint
        ? `${id}-hint`
        : undefined;
    const classes = [
      "rounded-lg border border-border bg-surface px-3 py-2 text-sm text-ink",
      "focus:outline-none focus:ring-2 focus:ring-accent",
      error ? "border-danger" : "",
      className ?? "",
    ]
      .filter(Boolean)
      .join(" ");
    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label htmlFor={id} className="text-sm text-ink-muted">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={id}
          aria-describedby={describedBy}
          aria-invalid={error ? true : undefined}
          className={classes}
          {...rest}
        />
        {hint && !error && (
          <p id={`${id}-hint`} className="text-xs text-ink-muted">
            {hint}
          </p>
        )}
        {error && (
          <p id={`${id}-error`} className="text-xs text-danger">
            {error}
          </p>
        )}
      </div>
    );
  },
);
Textarea.displayName = "Textarea";
