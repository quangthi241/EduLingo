import type { ReactNode } from "react";
import { TopNav } from "./TopNav";
import { TabBar } from "./TabBar";
import { ContextualRail } from "./ContextualRail";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-[color:var(--color-canvas)] text-[color:var(--color-ink)]">
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:absolute focus:left-3 focus:top-3 focus:z-50 focus:rounded focus:bg-[color:var(--color-accent)] focus:px-3 focus:py-2 focus:text-[color:var(--color-accent-ink)]"
      >
        Skip to content
      </a>
      <TopNav />
      <div className="mx-auto flex w-full max-w-[76rem] flex-1">
        <ContextualRail />
        <main
          id="main"
          className="flex-1 px-5 py-8 pb-28 md:px-10 md:py-12 md:pb-16"
        >
          {children}
        </main>
      </div>
      <footer className="mt-auto hidden border-t border-[color:var(--color-border)] md:block">
        <div className="mx-auto flex max-w-[76rem] items-baseline justify-between gap-4 px-10 py-5 text-xs text-[color:var(--color-ink-subtle)]">
          <p className="dateline text-[color:var(--color-ink-muted)]">
            EduLingo AI &mdash; a private coach for measurable fluency.
          </p>
          <p className="eyebrow">Vol. I &middot; No. 1</p>
        </div>
      </footer>
      <TabBar />
    </div>
  );
}
