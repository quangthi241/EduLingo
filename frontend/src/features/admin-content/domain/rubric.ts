import type { Rubric } from "@/features/library/domain/pieces";

export const DEFAULT_CEFR_RUBRIC: Rubric = {
  criteria: [
    {
      name: "Task achievement",
      description: "Addresses the prompt fully and relevantly.",
      minScore: 1,
      maxScore: 5,
    },
    {
      name: "Coherence",
      description: "Ideas are organised and signposted clearly.",
      minScore: 1,
      maxScore: 5,
    },
    {
      name: "Range",
      description: "Uses varied grammar and vocabulary appropriate to level.",
      minScore: 1,
      maxScore: 5,
    },
    {
      name: "Accuracy",
      description: "Grammar, spelling, and pronunciation are accurate.",
      minScore: 1,
      maxScore: 5,
    },
  ],
};
