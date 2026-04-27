import { Masthead } from "@shared/ui/Masthead";
export function BriefHeader({
  date,
  goalLabel,
}: {
  date: Date;
  goalLabel: string;
}) {
  return <Masthead date={date} goalLabel={goalLabel} />;
}
