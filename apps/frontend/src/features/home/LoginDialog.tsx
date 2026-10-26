import { useEffect, useRef } from "react";
import styles from "./LoginDialog.module.css";

export function LoginDialog({ onClose }: { onClose: () => void }) {
  const emailRef = useRef<HTMLInputElement>(null);
  useEffect(() => { emailRef.current?.focus(); const closeOnEscape = (event: KeyboardEvent) => event.key === "Escape" && onClose(); window.addEventListener("keydown", closeOnEscape); return () => window.removeEventListener("keydown", closeOnEscape); }, [onClose]);
  return <div className={styles.backdrop} onMouseDown={onClose}><section aria-labelledby="login-title" aria-modal="true" className={styles.dialog} onMouseDown={(event) => event.stopPropagation()} role="dialog"><button aria-label="Fechar" className={styles.close} onClick={onClose} type="button">×</button><p>ACESSO GEOSENSE</p><h2 id="login-title">Entre no Hub</h2><span>O acesso estará disponível quando a autenticação for configurada.</span><label htmlFor="email">E-mail</label><input id="email" placeholder="nome@exemplo.com" ref={emailRef} type="email" /><label htmlFor="password">Senha</label><input id="password" placeholder="••••••••" type="password" /><button onClick={onClose} type="button">Continuar</button></section></div>;
}
