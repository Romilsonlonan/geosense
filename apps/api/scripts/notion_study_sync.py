"""Synchronize local StudyGeoSense Markdown chapters to an organized Notion hub.

Usage: python scripts/notion_study_sync.py --apply
Without --apply it only prints the planned changes.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[3]
STUDY_DIRECTORY = ROOT / "StudyGeoSense"
NOTION_API = "https://api.notion.com/v1"
HUB_TITLE = "StudyGeoSense — Guia de Estudos"
load_dotenv(ROOT / ".env")


def markdown_blocks(markdown: str) -> list[dict[str, Any]]:
    """Convert headings, paragraphs and unordered list items to Notion blocks."""
    blocks: list[dict[str, Any]] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("### "):
            kind, text = "heading_3", line[4:]
        elif line.startswith("## "):
            kind, text = "heading_2", line[3:]
        elif line.startswith("# "):
            kind, text = "heading_1", line[2:]
        elif line.startswith("- "):
            kind, text = "bulleted_list_item", line[2:]
        else:
            kind, text = "paragraph", line
        blocks.append({"object": "block", "type": kind, kind: {"rich_text": [{"type": "text", "text": {"content": text}}]}})
    return blocks


def chapter_title(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").title()


class NotionStudySync:
    def __init__(self, token: str, parent_page_id: str, notion_version: str) -> None:
        self.parent_page_id = parent_page_id
        self.client = httpx.Client(
            base_url=NOTION_API,
            headers={"Authorization": f"Bearer {token}", "Notion-Version": notion_version, "Content-Type": "application/json"},
            timeout=30,
        )

    def child_pages(self, parent_page_id: str) -> dict[str, str]:
        """Return direct child pages indexed by their visible title."""
        response = self.client.get(f"/blocks/{parent_page_id}/children", params={"page_size": 100})
        response.raise_for_status()
        return {
            result["child_page"]["title"]: result["id"]
            for result in response.json()["results"]
            if result["type"] == "child_page"
        }

    def create_page(self, parent_page_id: str, title: str) -> str:
        response = self.client.post("/pages", json={"parent": {"page_id": parent_page_id}, "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}}})
        response.raise_for_status()
        return response.json()["id"]

    def append_blocks(self, page_id: str, blocks: list[dict[str, Any]]) -> None:
        for start in range(0, len(blocks), 100):
            append = self.client.patch(f"/blocks/{page_id}/children", json={"children": blocks[start:start + 100]})
            append.raise_for_status()

    def ensure_hub(self) -> tuple[str, bool]:
        existing = self.child_pages(self.parent_page_id)
        if HUB_TITLE in existing:
            return existing[HUB_TITLE], False
        hub_id = self.create_page(self.parent_page_id, HUB_TITLE)
        self.append_blocks(hub_id, markdown_blocks(
            "# Guia de Estudos GeoSense\n\n"
            "Este hub reúne os capítulos de estudo gerados durante a evolução do projeto. "
            "Cada capítulo descreve decisões, código, testes e limites técnicos.\n\n"
            "## Como usar\n\n"
            "- Navegue pelos capítulos abaixo na ordem sugerida.\n"
            "- O conteúdo é sincronizado a partir de `StudyGeoSense/` no repositório local.\n"
            "- Anotações complementares podem ser feitas diretamente em cada página."
        ))
        return hub_id, True

    def create_chapter(self, hub_page_id: str, title: str, content: str) -> None:
        page_id = self.create_page(hub_page_id, title)
        blocks = markdown_blocks(content)
        self.append_blocks(page_id, blocks)


def required_environment() -> tuple[str, str, str]:
    token = os.getenv("NOTION_TOKEN", "")
    parent_id = os.getenv("NOTION_PARENT_PAGE_ID", "")
    version = os.getenv("NOTION_VERSION", "2022-06-28")
    if not token or not parent_id:
        raise SystemExit("Defina NOTION_TOKEN e NOTION_PARENT_PAGE_ID no arquivo .env antes de sincronizar.")
    return token, parent_id, version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Cria capítulos que ainda não existam no Notion.")
    args = parser.parse_args()
    chapters = sorted(STUDY_DIRECTORY.glob("*.md"))
    if not chapters:
        raise SystemExit(f"Nenhum capítulo encontrado em {STUDY_DIRECTORY}")
    if not args.apply:
        print(f"Prévia — nenhum conteúdo será enviado. Estrutura planejada:\n- {HUB_TITLE}")
        print("\n".join(f"  - {chapter_title(path)}" for path in chapters))
        return
    token, parent_id, version = required_environment()
    sync = NotionStudySync(token, parent_id, version)
    hub_id, created = sync.ensure_hub()
    print(f"{'Criado' if created else 'Reutilizado'} hub: {HUB_TITLE}")
    existing = sync.child_pages(hub_id)
    for chapter in chapters:
        title = chapter_title(chapter)
        if title in existing:
            print(f"Ignorado (já existe): {title}")
            continue
        sync.create_chapter(hub_id, title, chapter.read_text(encoding="utf-8"))
        print(f"Criado: {title}")


if __name__ == "__main__":
    main()
