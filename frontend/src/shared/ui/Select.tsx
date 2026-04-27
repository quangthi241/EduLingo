import { SelectHTMLAttributes, forwardRef } from "react";

export type SelectOption = { value: string; label: string };

type Props = Omit<SelectHTMLAttributes<HTMLSelectElement>, "children"> & {
  label?: string;
  options: SelectOption[];
  error?: string;
  hint?: string;
  placeholder?: string;
};

export const Select = forwardRef<HTMLSelectElement, Props>(
  (
    { label, options, error, hint, placeholder, id, className, ...rest },
    ref,
  ) => {
    const describedBy = error ? `${id}-error` : hint ? `${id}-hint` : undefined;
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
        <select
          ref={ref}
          id={id}
          aria-describedby={describedBy}
          aria-invalid={error ? true : undefined}
          className={classes}
          {...rest}
        >
          {placeholder && <option value="">{placeholder}</option>}
          {options.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>
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
Select.displayName = "Select";
