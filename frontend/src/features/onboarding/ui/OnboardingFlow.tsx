"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@shared/api/client";
import { GoalPicker } from "./GoalPicker";
import { ContextStep, type ContextStepValue } from "./ContextStep";
import { PlacementIntro } from "./PlacementIntro";
import { getPreset, type GoalPreset } from "../domain/presets";

type Step = "goal" | "context" | "placement";

export function OnboardingFlow() {
  const router = useRouter();
  const [step, setStep] = useState<Step>("goal");
  const [goalId, setGoalId] = useState<GoalPreset["id"] | null>(null);
  const [context, setContext] = useState<ContextStepValue | null>(null);

  async function finalize() {
    if (!goalId || !context) return;
    await apiFetch("/api/auth/me", {
      method: "PATCH",
      body: JSON.stringify({
        goalId,
        minutesPerDay: context.minutesPerDay,
        startingHint: context.startingHint,
      }),
    });
    router.push("/placement-intro");
  }

  if (step === "goal") {
    return (
      <GoalPicker
        onSelect={(id) => {
          setGoalId(id);
          setStep("context");
        }}
      />
    );
  }
  if (step === "context") {
    const suggested = goalId ? getPreset(goalId)!.minutesPerDay : 20;
    return (
      <ContextStep
        suggestedMinutes={suggested}
        onNext={(value) => {
          setContext(value);
          setStep("placement");
        }}
      />
    );
  }
  return <PlacementIntro onBegin={finalize} />;
}
