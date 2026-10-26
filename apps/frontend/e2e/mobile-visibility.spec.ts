import { expect, test } from "@playwright/test";

test("oculta o globo decorativo no celular", async ({ page }) => {
  await page.setViewportSize({ width: 412, height: 924 });
  await page.goto("/");
  await expect(page.getByRole("img", { name: /Terra ilustrativa/i })).toBeHidden();
});
