import { ChangeEvent, InputHTMLAttributes, forwardRef } from "react";

type Props = Omit<InputHTMLAttributes<HTMLInputElement>, "type" | "onChange"> & {
  label?: string;
  error?: string;
  hint?: string;
  onFileChange?: (file: File | null) => void;
};

export const FileInput = forwardRef<HTMLInputElement, Props>(
  ({ label, error, hint, id, className, onFileChange, ...rest }, ref) => {
    const handle = (e: ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0] ?? null;
      onFileChange?.(file);
    };
    const describedBy = error ? `${id}-error` : hint ? `${id}-hint` : undefined;
    const classes = ["text-sm text-ink", className ?? ""]
      .filter(Boolean)
      .join(" ");
    return (
      <div className="flex flex-col gap-1">
        {label && (
          <label htmlFor={id} className="text-sm text-ink-muted">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={id}
          type="file"
          onChange={handle}
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
FileInput.displayName = "FileInput";
