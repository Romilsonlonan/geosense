from scripts.notion_study_sync import markdown_blocks


def test_markdown_blocks_preserves_supported_structures() -> None:
    blocks = markdown_blocks("# Título\n\nTexto\n- Item")

    assert [block["type"] for block in blocks] == ["heading_1", "paragraph", "bulleted_list_item"]
    assert blocks[0]["heading_1"]["rich_text"][0]["text"]["content"] == "Título"
