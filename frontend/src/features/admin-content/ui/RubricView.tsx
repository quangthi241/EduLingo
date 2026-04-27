import { DEFAULT_CEFR_RUBRIC } from "../domain/rubric";

export function RubricView() {
  return (
    <section className="rounded-xl border border-border p-4">
      <h3 className="text-sm font-medium">CEFR rubric (1–5 per criterion)</h3>
      <dl className="mt-3 grid gap-3 md:grid-cols-2">
        {DEFAULT_CEFR_RUBRIC.criteria.map((c) => (
          <div key={c.name}>
            <dt className="text-sm font-medium">{c.name}</dt>
            <dd className="text-sm text-ink-muted">{c.description}</dd>
          </div>
        ))}
      </dl>
    </section>
  );
}
