import { ProgressHero } from "./ProgressHero";
import { SkillMeter } from "./SkillMeter";

const SKILLS = [
  { name: "Listening", level: "B1", target: "B2", pct: 0.4 },
  { name: "Reading", level: "B2", target: "B2", pct: 0.8 },
  { name: "Speaking", level: "B1", target: "B2", pct: 0.3 },
  { name: "Writing", level: "B1", target: "B2", pct: 0.5 },
  { name: "Grammar", level: "B1", target: "B2", pct: 0.55 },
  { name: "Vocabulary", level: "B2", target: "B2", pct: 0.7 },
];

const RECENT = [
  { date: "21 Apr", title: "The slow erosion of coastlines", kind: "Reading piece", result: "B2 · held" },
  { date: "20 Apr", title: "Past perfect with 'by the time'", kind: "Grammar drill", result: "B1 · progressing" },
  { date: "19 Apr", title: "Night Radio", kind: "Listening piece", result: "B1 · progressing" },
  { date: "17 Apr", title: "Academic words — weekly batch", kind: "Vocabulary deck", result: "+12 mastered" },
];

export function ProgressView() {
  return (
    <div className="mx-auto flex max-w-[72ch] flex-col gap-14">
      <ProgressHero days={14} cefr="B1+" />

      <section
        id="skills"
        aria-labelledby="skills-heading"
        className="flex flex-col gap-5 border-t border-[color:var(--color-rule)] pt-10"
      >
        <header className="flex items-baseline justify-between gap-4">
          <h2 id="skills-heading" className="eyebrow">
            Skills, placed against target
          </h2>
          <span className="caption tabular text-[color:var(--color-ink-subtle)]">
            target: B2
          </span>
        </header>
        <div className="flex flex-col gap-4">
          {SKILLS.map((s) => (
            <SkillMeter key={s.name} {...s} />
          ))}
        </div>
      </section>

      <section
        id="history"
        aria-labelledby="history-heading"
        className="flex flex-col gap-4 border-t border-[color:var(--color-rule)] pt-10"
      >
        <h2 id="history-heading" className="eyebrow">
          Recent work
        </h2>
        <ul className="flex flex-col">
          {RECENT.map((r, i) => (
            <li
              key={i}
              className="grid grid-cols-[auto,1fr,auto] items-baseline gap-x-5 gap-y-0.5 border-b border-[color:var(--color-rule)] py-4 last:border-b-0"
            >
              <span className="dateline tabular text-sm text-[color:var(--color-ink-subtle)]">
                {r.date}
              </span>
              <div className="flex flex-col gap-0.5">
                <p className="font-display text-base text-[color:var(--color-ink)]">
                  {r.title}
                </p>
                <p className="caption">{r.kind}</p>
              </div>
              <span className="caption tabular text-[color:var(--color-ink-muted)] whitespace-nowrap">
                {r.result}
              </span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
