// Runs before paint to set data-theme on <html>, preventing flash.
// Reads localStorage("edu-theme") then falls back to prefers-color-scheme.
export function ThemeScript() {
  const src = `(() => {
    try {
      const stored = localStorage.getItem('edu-theme');
      const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = stored ?? (systemDark ? 'dark' : 'light');
      document.documentElement.dataset.theme = theme;
    } catch {}
  })();`;
  return <script dangerouslySetInnerHTML={{ __html: src }} />;
}
