import Link from "next/link";

const SKILLS = [
  { name: "Listening", blurb: "Transcript-paced comprehension, without captions as crutches." },
  { name: "Reading", blurb: "Long-form pieces chosen for your level, with assists you can hide." },
  { name: "Speaking", blurb: "Prompts that expect real sentences, graded on form and clarity." },
  { name: "Writing", blurb: "Short, honest responses. Edited once, explained once." },
];

export default function MarketingPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col gap-16 px-6 py-20">
      <header className="flex flex-col gap-6">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          EduLingo AI
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-5xl font-semibold leading-[1.05] tracking-tight sm:text-6xl">
          A private language coach that treats you like an adult.
        </h1>
        <p className="max-w-[60ch] text-lg text-[color:var(--color-ink-muted)]">
          CEFR-aligned pathways across four skills, plus grammar and vocabulary
          that are pulled through whatever you read, listen to, or say. No
          streaks. No cartoons.
        </p>
        <div>
          <Link
            href="/login"
            className="inline-flex items-center rounded-full bg-[color:var(--color-accent)] px-6 py-3 text-base font-medium text-[color:var(--color-accent-ink)] transition"
          >
            Start placement
          </Link>
        </div>
      </header>

      <section className="grid gap-10 border-t border-[color:var(--color-border)] pt-12 sm:grid-cols-2">
        {SKILLS.map((s) => (
          <article key={s.name} className="flex flex-col gap-2">
            <h2 className="font-[family-name:var(--font-literata)] text-xl font-semibold">
              {s.name}
            </h2>
            <p className="text-[color:var(--color-ink-muted)]">{s.blurb}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
