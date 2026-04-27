export interface NavItem {
  label: string;
  href: string;
  /** single glyph drawn in-line, no icon library */
  glyph: string;
}

export const NAV_ITEMS: readonly NavItem[] = [
  { label: "Today", href: "/today", glyph: "◆" },
  { label: "Library", href: "/library", glyph: "❏" },
  { label: "Review", href: "/review", glyph: "↻" },
  { label: "Progress", href: "/progress", glyph: "▲" },
] as const;
