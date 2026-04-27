import { TodayBrief, type TodayBriefData } from "@features/today/ui/TodayBrief";

const MOCK: TodayBriefData = {
  date: new Date(),
  goalLabel: "IELTS 7.0",
  intake: { title: "The slow erosion of coastlines", minutes: 8, cefr: "B2" },
  practice: { grammar: "Past perfect after 'by the time'", vocab: ["erode", "sediment", "mitigation"] },
  produce: { prompt: "Summarise the main argument in 4 sentences." },
  reflection: "What was the writer's strongest claim?",
};

export default function TodayPage() {
  return <TodayBrief data={MOCK} />;
}
