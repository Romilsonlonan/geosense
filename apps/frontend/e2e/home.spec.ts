import { expect, test } from "@playwright/test";

test("permite abrir o assistente na página inicial", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Começar" }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await page.getByRole("button", { name: "Fechar" }).click();
  await expect(page.getByRole("dialog")).toBeHidden();
});
