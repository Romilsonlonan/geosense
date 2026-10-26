"""
Hook de pre-commit: detecta PII hardcoded em arquivos Python e TypeScript.

Entidades que bloqueiam: EMAIL_ADDRESS, PHONE_NUMBER, BR_CPF
Entidades que avisam:    PERSON, LOCATION

Bypasses:
  - Prefixo FAKE_  →  email = "FAKE_user@example.com"
  - Comentário     →  valor = "dado"  # noqa: presidio
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

BLOCKED_ENTITIES = {"EMAIL_ADDRESS", "PHONE_NUMBER", "BR_CPF"}
WARN_ENTITIES = {"PERSON", "LOCATION"}

BYPASS_COMMENT = re.compile(r"#\s*noqa:\s*presidio", re.IGNORECASE)
FAKE_PREFIX = re.compile(r"FAKE_", re.IGNORECASE)

SKIP_LINE_PATTERNS = [
    re.compile(p) for p in [
        r"^\s*(import|from|def |class |#)",
        r"^\s*logger\.",
        r"placeholder|example\.com|test@",
    ]
]


def _load_analyzer():
    try:
        from presidio_analyzer import AnalyzerEngine
        from presidio_analyzer.nlp_engine import NlpEngineProvider
        try:
            provider = NlpEngineProvider(nlp_configuration={
                "nlp_engine_name": "spacy",
                "models": [{"lang_code": "pt", "model_name": "pt_core_news_sm"}],
            })
            engine = AnalyzerEngine(nlp_engine=provider.create_engine(), supported_languages=["pt"])
            engine.analyze(text="teste", language="pt")
            return engine, "pt"
        except Exception:
            pass
        return AnalyzerEngine(), "en"
    except ImportError:
        return None, None


def scan_file(path: Path, analyzer, language: str) -> list[tuple[int, str, str]]:
    violations: list[tuple[int, str, str]] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for lineno, line in enumerate(lines, start=1):
        if BYPASS_COMMENT.search(line) or FAKE_PREFIX.search(line):
            continue
        if any(p.search(line) for p in SKIP_LINE_PATTERNS):
            continue
        for content in re.findall(r'["\']([^"\']{6,})["\']', line):
            for result in analyzer.analyze(
                text=content, language=language,
                entities=list(BLOCKED_ENTITIES | WARN_ENTITIES),
            ):
                if result.score >= 0.6:
                    violations.append((lineno, result.entity_type, content[result.start:result.end]))
    return violations


def main(argv: list[str] | None = None) -> int:
    files = argv if argv is not None else sys.argv[1:]
    if not files:
        return 0
    analyzer, language = _load_analyzer()
    if analyzer is None:
        print("presidio_hook: presidio-analyzer não encontrado — instale no grupo dev", file=sys.stderr)
        return 0
    errors, warnings = [], []
    for file_arg in files:
        path = Path(file_arg)
        if not path.exists():
            continue
        for lineno, entity, snippet in scan_file(path, analyzer, language):
            msg = f"  {path}:{lineno} [{entity}] → {snippet!r}"
            (errors if entity in BLOCKED_ENTITIES else warnings).append(msg)
    if warnings:
        print("presidio_hook: AVISO — possível PII (não bloqueia):\n" + "\n".join(warnings))
    if errors:
        print("presidio_hook: BLOQUEADO — PII detectado:\n" + "\n".join(errors))
        print("\n  → Remova os dados pessoais do código.")
        print("  → Para dados fictícios: prefixe com FAKE_")
        print("  → Para falso positivo:  # noqa: presidio")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
