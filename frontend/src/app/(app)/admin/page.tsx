import Link from "next/link";

export default function AdminLanding() {
  return (
    <section>
      <h1 className="text-xl font-semibold">Admin</h1>
      <p className="mt-2 text-sm text-ink-muted">
        Manage the content library.
      </p>
      <div className="mt-6 flex gap-3">
        <Link
          href="/admin/content"
          className="rounded-xl border border-border px-4 py-2 text-sm hover:bg-surface"
        >
          Go to content
        </Link>
      </div>
    </section>
  );
}
