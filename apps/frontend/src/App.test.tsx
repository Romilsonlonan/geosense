import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { App } from "./App";
afterEach(cleanup);
describe("GeoSense home", () => { it("troca o domínio", () => { render(<App />); fireEvent.click(screen.getByRole("button", { name: /Sismologia/ })); expect(screen.getByRole("heading", { name: "Sismologia" })).toBeInTheDocument(); }); it("abre e fecha o assistente", () => { render(<App />); fireEvent.click(screen.getByRole("button", { name: "Começar" })); expect(screen.getByRole("dialog")).toBeInTheDocument(); fireEvent.click(screen.getByRole("button", { name: "Fechar" })); expect(screen.queryByRole("dialog")).not.toBeInTheDocument(); }); });
