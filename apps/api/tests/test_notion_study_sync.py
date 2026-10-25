from scripts.notion_study_sync import HUB_TITLE, chapter_title, markdown_blocks


def test_markdown_blocks_preserves_supported_structures() -> None:
    blocks = markdown_blocks("# Título\n\nTexto\n- Item")

    assert [block["type"] for block in blocks] == ["heading_1", "paragraph", "bulleted_list_item"]
    assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == "Título"


def test_chapter_title_uses_the_markdown_heading(tmp_path) -> None:
    chapter = tmp_path / "02-home-interface.md"
    chapter.write_text("# Home e interface\n", encoding="utf-8")

    assert chapter_title(chapter) == "Home e interface"
    assert HUB_TITLE == "StudyGeoSense — Guia de Estudos"
