export type PieceKind = "reading" | "listening" | "speaking" | "writing";
export type CefrLevel = "A1" | "A2" | "B1" | "B2" | "C1";
export type Topic =
  | "travel"
  | "business"
  | "daily-life"
  | "academic"
  | "culture"
  | "science";
export type PieceStatus = "draft" | "published" | "archived";

export type MCQ = {
  question: string;
  choices: string[];
  correctIndex: number;
  rationale: string;
};

export type ShortAnswer = { prompt: string; gradingNotes: string };

export type MediaRef = {
  storageKey: string;
  mimeType: string;
  durationSeconds: number | null;
};

export type RubricCriterion = {
  name: string;
  description: string;
  minScore: number;
  maxScore: number;
};

export type Rubric = { criteria: RubricCriterion[] };

export type ReadingBody = {
  kind: "reading";
  text: string;
  mcq: MCQ[];
  shortAnswer: ShortAnswer;
};

export type ListeningBody = {
  kind: "listening";
  audioRef: MediaRef | null;
  audioUrl: string | null;
  transcript: string;
  mcq: MCQ[];
  shortAnswer: ShortAnswer;
};

export type SpeakingBody = {
  kind: "speaking";
  prompt: string;
  referenceAudioRef: MediaRef | null;
  referenceAudioUrl: string | null;
  rubric: Rubric;
};

export type WritingBody = {
  kind: "writing";
  prompt: string;
  exemplar: string | null;
  rubric: Rubric;
};

export type PieceBody =
  | ReadingBody
  | ListeningBody
  | SpeakingBody
  | WritingBody;

export type Piece = {
  id: string;
  slug: string;
  title: string;
  cefr: CefrLevel;
  minutes: number;
  kind: PieceKind;
  topic: Topic;
  status: PieceStatus;
  source: "editorial" | "llm_generated";
  createdAt: string;
  updatedAt: string;
  publishedAt: string | null;
  body: PieceBody;
};

export type PiecePage = {
  items: Piece[];
  nextCursor: string | null;
};
