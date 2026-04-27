import { test, expect, type Page } from "@playwright/test";

const ADMIN_EMAIL = process.env.E2E_ADMIN_EMAIL ?? "admin@edulingo.ai";
const ADMIN_PASSWORD = process.env.E2E_ADMIN_PASSWORD ?? "Admin#12345";
const LEARNER_EMAIL = process.env.E2E_LEARNER_EMAIL ?? "learner@edulingo.ai";
const LEARNER_PASSWORD = process.env.E2E_LEARNER_PASSWORD ?? "Learner#12345";

async function login(page: Page, email: string, password: string) {
  await page.goto("/login");
  await page.getByLabel(/email/i).fill(email);
  await page.getByLabel(/password/i).fill(password);
  await page.getByRole("button", { name: /sign in|log in/i }).click();
  await page.waitForURL(/\/(today|profile|library)/);
}

async function logout(page: Page) {
  await page.goto("/profile");
  const signOut = page.getByRole("button", { name: /sign out/i });
  if (await signOut.isVisible()) {
    await signOut.click();
    await page.waitForURL(/\/login|\/$/);
  } else {
    await page.context().clearCookies();
  }
}

test.describe("admin content module", () => {
  test("admin creates + publishes a reading piece; learner sees it", async ({ page }) => {
    const slug = `e2e-reading-${Date.now()}`;

    await login(page, ADMIN_EMAIL, ADMIN_PASSWORD);
    await page.goto("/admin/content/new");

    // Pick reading
    await page.getByRole("link", { name: /reading/i }).click();
    await page.waitForURL(/\/admin\/content\/new\?kind=reading/);

    // Meta
    await page.getByLabel(/slug/i).fill(slug);
    await page.getByLabel(/title/i).fill("E2E Reading");
    await page.getByLabel(/cefr/i).selectOption("B1");
    await page.getByLabel(/minutes/i).fill("5");
    await page.getByLabel(/topic/i).selectOption("daily-life");

    // Body
    await page.getByLabel(/passage/i).fill(
      "A short passage for end-to-end verification of the content module."
    );

    // Fill the 3 seeded MCQ rows
    for (let i = 1; i <= 3; i++) {
      await page.getByLabel(new RegExp(`^Question ${i}$`)).fill(`Q${i}?`);
    }

    await page.getByRole("button", { name: /save draft/i }).click();
    await page.waitForURL(/\/admin\/content\/[0-9a-f-]{36}$/);

    // Publish
    await page.getByRole("button", { name: /^publish$/i }).click();
    await expect(page.getByText(/published/i).first()).toBeVisible();

    // Swap to learner
    await logout(page);
    await login(page, LEARNER_EMAIL, LEARNER_PASSWORD);

    // Library list shows it
    await page.goto("/library");
    await expect(page.getByRole("link", { name: /e2e reading/i })).toBeVisible();

    // Detail page renders
    await page.getByRole("link", { name: /e2e reading/i }).click();
    await page.waitForURL(new RegExp(`/library/${slug}$`));
    await expect(page.getByRole("heading", { name: /e2e reading/i })).toBeVisible();
    await expect(page.getByText(/verification of the content module/i)).toBeVisible();
  });

  test("non-admin hitting /admin is redirected to /today", async ({ page }) => {
    await login(page, LEARNER_EMAIL, LEARNER_PASSWORD);
    await page.goto("/admin");
    await page.waitForURL(/\/today$/);
  });
});
