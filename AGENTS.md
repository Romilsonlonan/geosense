# GeoSense — instruções para agentes de IA

> Leia este arquivo inteiro antes de escrever qualquer código.
> Ele substitui o que você sabe sobre "boas práticas genéricas" — aqui valem as regras do projeto.

---

## 1. Princípio central: verifique antes de criar

Antes de escrever qualquer código novo, responda a estas perguntas na ordem:

1. **Já existe?** — Procure no projeto (`grep`, `FindSymbol`, leitura de arquivos) antes de criar.
2. **A stdlib resolve?** — Python (`dataclasses`, `pathlib`, `itertools`) e JS/TS nativo antes de uma lib.
3. **Uma dependência já instalada resolve?** — Verifique `pyproject.toml` e `package.json` primeiro.
4. **A menor mudança possível resolve?** — Prefira editar uma função existente a criar uma nova.

Se a resposta for sim para qualquer uma, use o que existe. Não crie duplicata.

---

## 2. Stack — nunca instale fora desta lista sem justificativa documentada

### Backend (Python 3.12 · uv · FastAPI)
```
fastapi · uvicorn[standard] · pydantic · httpx · python-dotenv
opentelemetry-api · opentelemetry-sdk · opentelemetry-instrumentation-fastapi
pytest  (dev)
```
- Gerenciador exclusivo: **uv**. Jamais crie ou restaure `requirements.txt`.
- Para adicionar: `uv add <pacote>` — nunca `pip install`.
- Fonte da verdade: `apps/api/pyproject.toml` + `uv.lock`.

### Frontend (React 18 · TypeScript · Vite)
```
react · react-dom · recharts · @deck.gl/core · @deck.gl/layers · @deck.gl/react
@react-three/fiber · @react-three/drei · three · cesium
tailwindcss · vite-plugin-cesium
vitest · @testing-library/react · @testing-library/jest-dom · playwright
```
- Antes de instalar qualquer lib nova: justifique lacuna, tamanho de bundle, manutenção e alternativa nativa.

---

## 3. Arquitetura do backend — nunca pule etapas

```
adapter → service → repository → schema
```

| Camada | O que faz | O que NÃO faz |
|---|---|---|
| adapter | Fala com fonte externa (HTTP, arquivo) | Nenhuma lógica de negócio |
| service | Regras do domínio, cálculos derivados | Não acessa banco diretamente |
| repository | Lê/escreve no banco | Nenhuma lógica de negócio |
| schema | Frozen dataclass `slots=True` | Não muda após construção |

**Invariante:** domínio nunca importa infraestrutura diretamente.

---

## 4. Arquitetura do frontend — fluxo de dependência

```
App.tsx → AskAIProvider → features/<dominio>/ → components/
```

- `components/` **nunca** importa de `features/`.
- Dados e tipos de domínio ficam em `features/`, nunca em `App.tsx`.
- Novos painéis de domínio implementam `DomainPanelProps` de `features/shared/`.
- `AskAIContext` é o único canal global de estado do assistente.

---

## 5. Dados — princípio "nenhum dado fabricado"

- Toda fonte externa documentada em `docs/data-sources/README.md` **antes** da integração.
- Observações, interpretações e métricas derivadas sempre rotuladas separadamente.
- Dados de demonstração em componentes levam label `ILUSTRAÇÃO — fonte pendente` na UI.
- Métricas derivadas (ex.: índice de fertilidade) têm sufixo `_derived` no nome da variável e no tipo.

---

## 6. Testes — escreva junto com o código, nunca depois

- **Backend:** toda função pura tem teste pytest. Execute: `uv run pytest`.
- **Frontend:** toda interação nova tem teste Vitest + Testing Library. Execute: `npm test`.
- **WebGL (R3F, deck.gl, CesiumJS):** use `vi.mock()` no arquivo de teste — jsdom não tem GPU.
  ```typescript
  vi.mock("./components/visuals/GlobeHero", () => ({ GlobeHero: () => null }));
  ```
- **Testes visuais de WebGL:** ficam em `e2e/` com Playwright (browser real).
- Diálogos respondem a `Escape`, têm `aria-modal` e `aria-labelledby`.

---

## 7. Segurança

- `ANTHROPIC_API_KEY` exclusivamente server-side. Nunca no frontend.
- `VITE_CESIUM_ION_TOKEN` vem de variável de ambiente, nunca hardcoded.
- Nenhum secret em arquivos versionados. Modelo: `.env.example` sem valores.

---

## 8. Branches — convenção hierárquica

Detalhes completos: `docs/branching-strategy.md`.

```
setup/initial        infra/initial        ci/initial
home-page/initial    feat/climate/initial feat/seismology/initial
feat/soil/initial    feat/vegetation/initial feat/hydrology/initial
feat/oceanography/initial feat/map-3d/initial
ai/rag-pipeline      ai/guardrails        ai/hermes-agent
```

- Nenhum commit direto em `main`.
- Branches `/initial` nunca são deletadas.
- Nomes descritivos: `setup/migrate-to-uv`, não `setup/update`.

---

## 9. Antes de finalizar qualquer tarefa

Execute na ordem:

```bash
# Backend
cd apps/api && uv run pytest

# Frontend
cd apps/frontend && npm test && npm run build

# Docs
mkdocs build --strict
```

Só entregue quando os três passarem sem novos erros.

---

## 10. Referências internas

| Documento | O que contém |
|---|---|
| `docs/architecture.md` | Stack completo, camadas, diagramas |
| `docs/frontend-architecture.md` | Organização de pastas, AskAIContext, regras de testes WebGL |
| `docs/branching-strategy.md` | Convenção de branches hierárquicas |
| `docs/data-sources/README.md` | Fontes externas documentadas |
| `agents/geosense-agent-policy.yml` | Invariantes e stack (formato de agente) |
| `agents/code-review-agent-policy.yml` | Checklist de PR e revisão |
