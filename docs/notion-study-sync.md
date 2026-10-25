# Sincronização dos estudos com Notion

1. Crie uma página-pai no Notion e compartilhe-a com a integração.
2. Em `.env`, preencha `NOTION_TOKEN` e `NOTION_PARENT_PAGE_ID`.
3. Confira a prévia: `cd apps/api && python scripts/notion_study_sync.py`.
4. Publique os capítulos ausentes: `python scripts/notion_study_sync.py --apply`.

O sincronizador cria a página-hub **StudyGeoSense — Guia de Estudos** dentro da página-pai configurada. Cada capítulo vira uma subpágina usando o título do seu Markdown, resultando em uma estrutura de navegação clara e ordenada.

Ele é idempotente: reutiliza o hub e ignora capítulos já existentes. Ele não atualiza nem apaga páginas, preservando anotações feitas no Notion.
