import Link from "next/link";
import { ReactNode } from "react";

export default function AdminLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex gap-8">
      <aside className="w-48 shrink-0 border-r border-border pr-4">
        <nav className="flex flex-col gap-2 text-sm">
          <Link href="/admin" className="hover:text-accent">
            Overview
          </Link>
          <Link href="/admin/content" className="hover:text-accent">
            Content
          </Link>
        </nav>
      </aside>
      <main className="flex-1 min-w-0">{children}</main>
    </div>
  );
}
