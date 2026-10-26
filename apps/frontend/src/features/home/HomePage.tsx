import { useState } from "react";
import { GlobeHero } from "../../components/visuals/GlobeHero";
import { domains } from "./home.data";
import { LoginDialog } from "./LoginDialog";
import type { Domain } from "./home.types";
import styles from "./HomePage.module.css";

export function HomePage() {
  const [activeDomain, setActiveDomain] = useState<Domain>("Clima");
  const [loginOpen, setLoginOpen] = useState(false);
  const selected = domains.find((domain) => domain.name === activeDomain)!;
  return <main className={styles.page}>
    <header className={styles.header}><a className={styles.brand} href="#inicio"><b>◎</b><span>GeoSense<small>GEOSCIENCE HUB</small></span></a><nav aria-label="Navegação principal"><a aria-current="page" href="#inicio">Início</a><a href="#explorar">Explorar</a><a href="#dados">Dados</a><a href="#simular">Simulações</a><a href="#estudos">Estudos</a></nav><div className={styles.actions}><button aria-label="Buscar" className={styles.search} type="button">⌕</button><button className={styles.login} onClick={() => setLoginOpen(true)} type="button">Entrar</button></div></header>
    <section className={styles.hero} id="inicio"><div className={styles.copy}><p>HUB DE CONHECIMENTO EM GEOCIÊNCIAS</p><h1>Explore. Understand.<br /><span>Simulate.</span></h1><strong>Dados reais, visualizações interativas, IA com fundamentos científicos e simulações com limites explícitos.</strong><div className={styles.ctas}><a href="#explorar">Explorar o Hub <b>→</b></a><button type="button">✦ Ask AI</button></div></div><GlobeHero /><aside className={styles.layers}><div><b>Terra em tempo real</b><span>●</span></div><p><i>☁</i> 22º Células (clima)</p><p><i>◒</i> Sismos (USGS)</p><p><i>≈</i> NDVI (NASA GIBS)</p><p><i>⌁</i> Ondas (Marine API)</p><small>ILUSTRAÇÃO — fonte pendente</small></aside></section>
    <section className={styles.domains} id="explorar">{domains.map((domain) => <button aria-pressed={activeDomain === domain.name} className={activeDomain === domain.name ? styles.active : ""} key={domain.name} onClick={() => setActiveDomain(domain.name)} type="button"><i>{domain.icon}</i><span><b>{domain.name}</b><small>{domain.detail}</small></span></button>)}</section>
    <section className={styles.preview} id="dados"><div><p>DOMÍNIO EM DESTAQUE</p><h2>{selected.icon} {selected.name}</h2><span>{selected.detail}. Selecione uma fonte documentada para começar uma análise rastreável.</span></div><aside><b>Fonte</b><span>Configurar integração</span><b>Proveniência</b><span>Pendente</span></aside></section>
    <section className={styles.values} id="simular"><article><b>◈ Fontes primeiro</b><span>Cobertura, licença e limitações explícitas.</span></article><article><b>⌘ Rastreabilidade</b><span>Observações e interpretações separadas.</span></article><article><b>↗ Pronto para explorar</b><span>Construa sobre dados verificáveis.</span></article></section>
    {loginOpen && <LoginDialog onClose={() => setLoginOpen(false)} />}
  </main>;
}
