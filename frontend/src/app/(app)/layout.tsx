import type { ReactNode } from "react";
import { AppShell } from "@shared/ui/app-shell/AppShell";

export default function AppShellLayout({ children }: { children: ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
