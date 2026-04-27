"use client";

import { useState } from "react";

export type Theme = "light" | "dark";

const STORAGE_KEY = "edu-theme";

function readTheme(): Theme {
  if (typeof document === "undefined") return "light";
  const value = document.documentElement.dataset.theme;
  return value === "dark" ? "dark" : "light";
}

export function useTheme(): { theme: Theme; setTheme: (t: Theme) => void } {
  // Lazy initializer reads DOM once on mount, avoiding setState-in-effect lint error
  const [theme, setState] = useState<Theme>(readTheme);

  function setTheme(next: Theme) {
    setState(next);
    document.documentElement.dataset.theme = next;
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      /* noop */
    }
  }

  return { theme, setTheme };
}
