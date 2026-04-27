export interface ReviewItem {
  id: string;
  kind: "grammar" | "vocabulary";
  cue: string;
  dueIn: string;
  /** What the learner should recall. For vocabulary this is a definition
   *  plus an example; for grammar this is a short rule + example line. */
  answer: string;
  example?: string;
}

export const REVIEW_ITEMS: ReviewItem[] = [
  {
    id: "g1",
    kind: "grammar",
    cue: "Past perfect after 'by the time'",
    dueIn: "now",
    answer:
      "One past action finishes before another begins. Use had + past participle for the earlier action.",
    example: "By the time the maps were updated, the coastline had already moved.",
  },
  {
    id: "v1",
    kind: "vocabulary",
    cue: "erode",
    dueIn: "now",
    answer: "To wear away gradually, especially by natural forces.",
    example: "Wind and rain slowly erode the soft rock of the cliff.",
  },
  {
    id: "v2",
    kind: "vocabulary",
    cue: "sediment",
    dueIn: "now",
    answer: "Matter that settles to the bottom of a liquid, or is carried and deposited by water or wind.",
    example: "The river carries sediment downstream each spring.",
  },
  {
    id: "g2",
    kind: "grammar",
    cue: "Reported speech with modals",
    dueIn: "tomorrow",
    answer:
      "In reported speech, can → could, will → would, may → might. Other modals usually stay the same.",
    example: "\"I can help\" → She said she could help.",
  },
  {
    id: "v3",
    kind: "vocabulary",
    cue: "mitigation",
    dueIn: "now",
    answer:
      "The action of reducing the severity of something unpleasant, especially a harm or risk.",
    example: "Planting dunes is the cheapest form of coastal mitigation.",
  },
];
