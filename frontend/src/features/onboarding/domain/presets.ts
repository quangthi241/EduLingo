export interface GoalPreset {
  id: "ielts" | "toefl" | "fluency" | "professional" | "travel";
  label: string;
  blurb: string;
  suggestedCefr: "A2" | "B1" | "B2" | "C1";
  minutesPerDay: 15 | 20 | 30 | 45;
}

export const GOAL_PRESETS: readonly GoalPreset[] = [
  { id: "ielts", label: "IELTS", blurb: "Target-band practice across the four skills with timed sections.", suggestedCefr: "B2", minutesPerDay: 45 },
  { id: "toefl", label: "TOEFL", blurb: "Academic reading and lectures, integrated speaking and writing.", suggestedCefr: "B2", minutesPerDay: 45 },
  { id: "fluency", label: "Everyday fluency", blurb: "Conversational range: common topics, opinions, short arguments.", suggestedCefr: "B1", minutesPerDay: 20 },
  { id: "professional", label: "Professional English", blurb: "Meetings, email, presentations — precise over ornate.", suggestedCefr: "B2", minutesPerDay: 20 },
  { id: "travel", label: "Travel", blurb: "Logistics, menus, small talk; confidence in public situations.", suggestedCefr: "A2", minutesPerDay: 15 },
] as const;

export function getPreset(id: string): GoalPreset | undefined {
  return GOAL_PRESETS.find((p) => p.id === id);
}
