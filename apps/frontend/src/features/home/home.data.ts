import type { DomainCard } from "./home.types";

export const domains: readonly DomainCard[] = [
  { name: "Clima", icon: "☁", detail: "Tempo, previsão e padrões" }, { name: "Sismologia", icon: "✦", detail: "Sismos, magnitude e risco" },
  { name: "Solo", icon: "◒", detail: "Propriedades e fertilidade" }, { name: "Vegetação", icon: "⌁", detail: "NDVI, desmatamento e foco" },
  { name: "Hidrologia", icon: "≈", detail: "Vazão, bacias e eventos" }, { name: "Oceanografia", icon: "◌", detail: "Ondas, marés e correntes" },
];
