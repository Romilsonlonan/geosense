import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { App } from "./App";

afterEach(cleanup);

describe("GeoSense home", () => {
  it("expõe a navegação e a marca da página", () => {
    render(<App />);
    expect(screen.getByRole("link", { name: /GeoSense/i })).toHaveAttribute("href", "#inicio");
    expect(screen.getByRole("link", { name: "Início" })).toHaveAttribute("aria-current", "page");
  });

  it("troca o domínio selecionado", () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: /Sismologia/ }));
    expect(screen.getByRole("button", { name: /Sismologia/ })).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByRole("heading", { name: /Sismologia/ })).toBeInTheDocument();
  });

  it("abre e fecha o login com Escape", () => {
    render(<App />);
    const login = screen.getByRole("button", { name: "Entrar" });
    fireEvent.click(login);
    expect(screen.getByRole("dialog", { name: "Entre no Hub" })).toBeInTheDocument();
    expect(screen.getByLabelText("E-mail")).toHaveFocus();
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("dialog", { name: "Entre no Hub" })).not.toBeInTheDocument();
  });
});
