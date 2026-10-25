# Coordenação de agentes

`geosense-agent-policy.yml` é a fonte única para responsabilidades dos agentes. As instruções especializadas devem referenciar este arquivo em vez de repetir políticas, evitando conflito e redundância.

Para Jira, a automação deve primeiro descobrir projeto, campos obrigatórios e transições. O acompanhamento de fluxo usa itens, builds e PRs; não deve estimar desempenho individual com base em atividade bruta.
