import { test, expect } from "@playwright/test";

test("marketing landing renders", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText(/private language coach/i);
  await expect(page.getByRole("link", { name: /start placement/i })).toBeVisible();
});

test("protected /today redirects to /login when unauthenticated", async ({ page }) => {
  await page.goto("/today");
  await expect(page).toHaveURL(/\/login\?next=%2Ftoday/);
});
