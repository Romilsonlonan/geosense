import { useState } from "react";

type Domain = "Clima" | "Sismologia" | "Solo" | "Vegetação" | "Hidrologia" | "Oceanografia";
const domains: { name: Domain; icon: string; detail: string }[] = [
  { name: "Clima", icon: "☁", detail: "Variáveis atmosféricas" }, { name: "Sismologia", icon: "✦", detail: "Eventos e frequência" },
  { name: "Solo", icon: "◒", detail: "Propriedades do terreno" }, { name: "Vegetação", icon: "⌁", detail: "Cobertura e contexto" },
  { name: "Hidrologia", icon: "≈", detail: "Água e risco" }, { name: "Oceanografia", icon: "◌", detail: "Condições marinhas" },
];

function Globe() { return <div className="globe-scene" aria-label="Globo terrestre ilustrativo" role="img"><div className="orbit one" /><div className="orbit two" /><div className="globe"><i className="land a" /><i className="land b" /><i className="land c" /></div><b className="star s1" /><b className="star s2" /></div>; }

export function App() {
  const [active, setActive] = useState<Domain>("Clima");
  const [askOpen, setAskOpen] = useState(false);
  const selected = domains.find((domain) => domain.name === active)!;
  return <main className="app-shell">
    <header className="topbar"><a className="brand" href="#inicio">◎ <span>GeoSense<small>GEOSCIENCE HUB</small></span></a><nav><a className="selected" href="#inicio">Início</a><a href="#explorar">Explorar</a><a href="#dados">Dados</a><a href="#simular">Simulações</a></nav><div className="actions"><button className="login">Entrar</button><button className="start" onClick={() => setAskOpen(true)}>Começar</button></div></header>
    <section className="hero" id="inicio"><div className="hero-copy"><p className="eyebrow">HUB DE CONHECIMENTO EM GEOCIÊNCIAS</p><h1>Explore. Understand.<br /><span>Simulate.</span></h1><p>Dados, análises e visualizações interativas. Um ambiente para compreender sistemas naturais com contexto, proveniência e limites explícitos.</p><div><button className="primary" onClick={() => document.querySelector("#explorar")?.scrollIntoView({ behavior: "smooth" })}>Explorar o Hub →</button><button className="secondary" onClick={() => setAskOpen(true)}>✦ Perguntar à IA</button></div></div><Globe /><aside className="layer"><p>● CAMADA ATIVA</p><b>Visão planetária</b><hr /><span>Fonte <em>configurar</em></span><span>Proveniência <em>pendente</em></span></aside></section>
    <section className="domain-strip" id="explorar">{domains.map((domain) => <button key={domain.name} className={active === domain.name ? "domain active" : "domain"} onClick={() => setActive(domain.name)}><i>{domain.icon}</i><span><b>{domain.name}</b><small>{domain.detail}</small></span><em>→</em></button>)}</section>
    <section className="workspace" id="dados"><article className="map panel"><header>● EXPLORAR DADOS <b>•••</b></header><div className="map-view"><div className="grid" /><i className="map-land x" /><i className="map-land y" /><i className="map-land z" /><strong>{selected.icon}</strong><p>Camada de visualização<br /><b>{selected.name}</b></p></div><footer>Modo de exploração <span>● Interface sem observações carregadas</span></footer></article><article className="context panel"><header>● CONTEXTO DO DOMÍNIO <b>•••</b></header><div><i>{selected.icon}</i><h2>{selected.name}</h2><p>{selected.detail}. Selecione uma fonte documentada para iniciar uma análise rastreável.</p><button onClick={() => setAskOpen(true)}>Abrir assistente →</button></div><footer>Estado: aguardando fonte <span>0 registros</span></footer></article></section>
    <section className="features" id="simular"><article><i>◈</i><h2>Fontes primeiro</h2><p>Cada integração nasce com licença, cobertura, atualização e limitações documentadas.</p></article><article><i>⌘</i><h2>Rastreabilidade</h2><p>Observação, interpretação e métricas derivadas permanecem claramente separadas.</p></article><article><i>↗</i><h2>Pronto para explorar</h2><p>Escolha um domínio e construa sua investigação sobre dados verificáveis.</p></article></section>
    {askOpen && <div className="backdrop" onMouseDown={() => setAskOpen(false)}><section className="dialog" role="dialog" aria-modal="true" aria-labelledby="ask-title" onMouseDown={(event) => event.stopPropagation()}><button className="close" aria-label="Fechar" onClick={() => setAskOpen(false)}>×</button><p className="eyebrow">ASSISTENTE GEOSENSE</p><h2 id="ask-title">Como posso orientar sua exploração?</h2><p>O assistente RAG será conectado apenas a fontes documentadas. Não gera dados observacionais.</p><label htmlFor="question">Sua pergunta</label><textarea id="question" placeholder="Ex.: Quais fontes são adequadas para investigar precipitação?" /><button className="primary" onClick={() => setAskOpen(false)}>Preparar consulta →</button></section></div>}
  </main>;
}
