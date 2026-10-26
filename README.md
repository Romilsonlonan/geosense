# GeoSense

> Explore. Understand. Simulate.

Hub full-stack de conhecimento em geociências, com visualização espacial, fontes rastreáveis e IA baseada em RAG para clima, sismologia, solo, vegetação, hidrologia e oceanografia.

## Princípios

- **Nenhum dado fabricado** — toda fonte externa documentada em `docs/data-sources/README.md` antes da integração.
- **Rastreabilidade** — observações, interpretações e métricas derivadas sempre separadas e rotuladas.
- **Credenciais server-side** — chaves e tokens exclusivamente em variáveis de ambiente, nunca no código.
- **Evolução incremental** — estrutura cresce conforme dependências e testes comprovem a necessidade.

## Stack

| Camada | Tecnologia |
|---|---|
| Frontend | React 18 · TypeScript · Vite · Tailwind CSS v4 |
| Visualização | recharts · deck.gl · CesiumJS · React Three Fiber |
| Backend | Python 3.12 · FastAPI · uv |
| Banco | PostgreSQL · PostGIS · pgvector |
| Observabilidade | OpenTelemetry (opt-in) |
| Testes | pytest · Vitest · Playwright |
| CI/CD | GitHub Actions |

## Setup

```bash
# 1. Banco de dados (PostgreSQL + PostGIS + pgvector)
docker compose up -d

# 2. Backend
cd apps/api
uv sync --dev
uv run uvicorn app.main:app --reload

# 3. Frontend
cd apps/frontend
npm ci
npm run dev
```

Variáveis de ambiente: copie `.env.example` para `.env` e preencha os valores.

## Estrutura

```
.
├── apps/
│   ├── api/          # FastAPI (Python 3.12 · uv)
│   └── frontend/     # React + Vite (TypeScript)
├── agents/           # Políticas de agentes de IA
├── docs/             # Documentação (MkDocs Material)
├── infrastructure/   # Docker, banco, infraestrutura
├── tools/            # Scripts utilitários (hooks, segurança)
├── AGENTS.md         # Instruções para agentes de IA (Bob, Codex, OpenRouter)
└── .pre-commit-config.yaml  # Hooks de segurança (detect-secrets, presidio)
```

## Domínios

Clima · Sismologia · Solo · Vegetação · Hidrologia · Oceanografia

Cada domínio segue a sequência: `adapter → service → repository → schema`.

## Documentação

```bash
# Servir localmente
uv tool run --from mkdocs-material mkdocs serve

# Build (usado no CI)
uv tool run --from mkdocs-material mkdocs build --strict
```

## Licença

Ainda não definida.
