# Sincronização dos estudos com Notion

1. Crie uma página-pai no Notion e compartilhe-a com a integração.
2. Em `.env`, preencha `NOTION_TOKEN` e `NOTION_PARENT_PAGE_ID`.
3. Confira a prévia: `cd apps/api && python scripts/notion_study_sync.py`.
4. Publique os capítulos ausentes: `python scripts/notion_study_sync.py --apply`.

O sincronizador é idempotente para capítulos existentes: ele cria apenas páginas-filhas cujo título ainda não esteja no pai. Ele não atualiza nem apaga páginas já existentes, preservando anotações feitas no Notion.
