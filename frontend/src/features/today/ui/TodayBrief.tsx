import { BriefHeader } from "./BriefHeader";
import { IntakeSection } from "./IntakeSection";
import { PracticeSection } from "./PracticeSection";
import { ProduceSection } from "./ProduceSection";
import { ReflectionPrompt } from "./ReflectionPrompt";

export interface TodayBriefData {
  date: Date;
  goalLabel: string;
  intake: { title: string; minutes: number; cefr: string };
  practice: { grammar: string; vocab: string[] };
  produce: { prompt: string };
  reflection: string;
}

export function TodayBrief({ data }: { data: TodayBriefData }) {
  return (
    <article className="mx-auto flex max-w-[68ch] flex-col gap-12">
      <BriefHeader date={data.date} goalLabel={data.goalLabel} />
      <p className="dateline text-lg text-[color:var(--color-ink-muted)]">
        A fifteen-minute reading, with practice and a short response.
        Nothing today is required &mdash; everything is chosen for your
        pathway toward {data.goalLabel}.
      </p>
      <div className="flex flex-col gap-14">
        <IntakeSection {...data.intake} />
        <PracticeSection {...data.practice} />
        <ProduceSection {...data.produce} />
      </div>
      <ReflectionPrompt prompt={data.reflection} />
    </article>
  );
}
