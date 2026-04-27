import { Suspense } from "react";
import { LoginForm } from "@features/auth/ui/LoginForm";

export default function LoginPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-sm flex-col justify-center gap-8 px-6 py-20">
      <header className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.18em] text-[color:var(--color-ink-subtle)]">
          Sign in
        </p>
        <h1 className="font-[family-name:var(--font-literata)] text-3xl font-semibold tracking-tight">
          Welcome back.
        </h1>
      </header>
      <Suspense fallback={null}>
        <LoginForm />
      </Suspense>
    </main>
  );
}
