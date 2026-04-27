export type {
  Piece,
  PiecePage,
  PieceBody,
  MCQ,
  ShortAnswer,
  MediaRef,
} from "@/features/library/domain/pieces";

export type AdminListFilter = {
  status?: "draft" | "published" | "archived";
  kind?: "reading" | "listening" | "speaking" | "writing";
  cefr?: "A1" | "A2" | "B1" | "B2" | "C1";
  topic?:
    | "travel"
    | "business"
    | "daily-life"
    | "academic"
    | "culture"
    | "science";
  cursor?: string;
  limit?: number;
};

export type CreatePieceInput = {
  kind: "reading" | "listening" | "speaking" | "writing";
  slug: string;
  title: string;
  cefr: string;
  minutes: number;
  topic: string;
  body: unknown;
};

export type UpdatePieceInput = Partial<{
  title: string;
  cefr: string;
  minutes: number;
  topic: string;
  body: unknown;
}>;

export type GenerateInput = {
  kind: "reading" | "listening" | "speaking" | "writing";
  cefr: string;
  topic: string;
  seedPrompt?: string;
};
