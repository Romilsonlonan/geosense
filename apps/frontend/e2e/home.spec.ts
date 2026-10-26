import { expect, test } from "@playwright/test";

test("permite abrir o login na página inicial", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Entrar" }).click();
  await expect(page.getByRole("dialog", { name: "Entre no Hub" })).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toBeHidden();
});

test("se reorganiza sem overflow horizontal no celular", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto("/");
  await expect(page.getByRole("heading", { name: /Explore\. Understand/i })).toBeVisible();
  const hasNoHorizontalOverflow = await page.locator("body").evaluate((body) => body.scrollWidth <= window.innerWidth);
  expect(hasNoHorizontalOverflow).toBe(true);
  await expect(page.getByText("Terra em tempo real")).toBeVisible();
});
