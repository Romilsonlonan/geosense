import styles from "./GlobeHero.module.css";

export function GlobeHero() {
  return <div aria-label="Terra ilustrativa girando, vista do espaço" className={styles.scene} role="img">
    <div aria-hidden className={styles.galaxy} />
    <div className={`${styles.orbit} ${styles.orbitOne}`} /><div className={`${styles.orbit} ${styles.orbitTwo}`} />
    <div className={styles.globe}><div className={styles.surface}><span className={`${styles.cloud} ${styles.cloudOne}`} /><span className={`${styles.land} ${styles.landOne}`} /><span className={`${styles.land} ${styles.landTwo}`} /><span className={`${styles.land} ${styles.landThree}`} /></div></div>
  </div>;
}
