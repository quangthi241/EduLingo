"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { useState, type FormEvent } from "react";
import { useLogin } from "../application/useAuth";
import { Field, Label, Input, FieldError } from "@shared/ui/Field";

export function LoginForm() {
  const router = useRouter();
  const params = useSearchParams();
  const next = params.get("next") ?? "/today";
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const login = useLogin();

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    await login.mutateAsync({ email, password });
    router.push(next);
  }

  return (
    <form onSubmit={handleSubmit} className="flex w-full max-w-sm flex-col gap-4">
      <Field>
        <Label htmlFor="email">Email</Label>
        <Input
          id="email"
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
        />
      </Field>
      <Field>
        <Label htmlFor="password">Password</Label>
        <Input
          id="password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
      </Field>
      {login.isError && (
        <FieldError>{(login.error as Error).message}</FieldError>
      )}
      <button
        type="submit"
        disabled={login.isPending}
        className="rounded-full bg-[color:var(--color-accent)] px-4 py-2 text-[color:var(--color-accent-ink)] disabled:opacity-50"
      >
        {login.isPending ? "Signing in…" : "Sign in"}
      </button>
    </form>
  );
}
