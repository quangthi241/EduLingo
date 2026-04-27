import { SessionShell } from "@features/session/ui/SessionShell";

export default async function SessionPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = await params;
  return <SessionShell sessionId={sessionId} />;
}
