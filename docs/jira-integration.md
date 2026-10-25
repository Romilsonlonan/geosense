# Integração com Jira

A automação do GeoSense usa apenas credenciais server-side (`JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_PROJECT_KEY`). O projeto e os campos obrigatórios devem ser descobertos antes de qualquer criação automática de work item.

Cada branch pode ser associada a um item Jira com o prefixo da chave (`GEO-123-page-home`). Métricas de fluxo devem ser derivadas do Jira e da CI, sem inferir esforço individual a partir de atividade bruta.
