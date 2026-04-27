import { GenerateWizard } from "@/features/admin-content/ui/GenerateWizard";

export default function Page() {
  return (
    <section className="flex flex-col gap-4">
      <h1 className="text-xl font-semibold">Generate a draft</h1>
      <GenerateWizard />
    </section>
  );
}
