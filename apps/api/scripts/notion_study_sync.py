"""Synchronize local StudyGeoSense Markdown chapters to child pages in Notion.

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
    return f"StudyGeoSense — {path.stem}"


class NotionStudySync:
    def __init__(self, token: str, parent_page_id: str, notion_version: str) -> None:
        self.parent_page_id = parent_page_id
        self.client = httpx.Client(
            base_url=NOTION_API,
            headers={"Authorization": f"Bearer {token}", "Notion-Version": notion_version, "Content-Type": "application/json"},
            timeout=30,
        )

    def existing_child_titles(self) -> set[str]:
        response = self.client.get(f"/blocks/{self.parent_page_id}/children", params={"page_size": 100})
        response.raise_for_status()
        return {
            result["child_page"]["title"]
            for result in response.json()["results"]
            if result["type"] == "child_page"
        }

    def create_chapter(self, title: str, content: str) -> None:
        response = self.client.post("/pages", json={"parent": {"page_id": self.parent_page_id}, "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}}})
        response.raise_for_status()
        page_id = response.json()["id"]
        blocks = markdown_blocks(content)
        for start in range(0, len(blocks), 100):
            append = self.client.patch(f"/blocks/{page_id}/children", json={"children": blocks[start:start + 100]})
            append.raise_for_status()


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
        print("Prévia — nenhum conteúdo será enviado. Use --apply para publicar:")
        print("\n".join(f"- {chapter_title(path)}" for path in chapters))
        return
    token, parent_id, version = required_environment()
    sync = NotionStudySync(token, parent_id, version)
    existing = sync.existing_child_titles()
    for chapter in chapters:
        title = chapter_title(chapter)
        if title in existing:
            print(f"Ignorado (já existe): {title}")
            continue
        sync.create_chapter(title, chapter.read_text(encoding="utf-8"))
        print(f"Criado: {title}")


if __name__ == "__main__":
    main()
