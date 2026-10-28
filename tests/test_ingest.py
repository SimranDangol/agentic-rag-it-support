from app.ingest import build_chunks


def test_build_chunks_splits_markdown_with_stable_source_ids(tmp_path):
    source = tmp_path / "guide.md"
    source.write_text(" ".join(f"word{i}" for i in range(250)), encoding="utf-8")

    chunks = build_chunks(tmp_path)

    assert len(chunks) > 1
    assert [chunk["id"] for chunk in chunks] == [
        f"guide.md-{i}" for i in range(len(chunks))
    ]
    assert all(chunk["source"] == "guide.md" for chunk in chunks)
    assert all(chunk["text"] for chunk in chunks)


def test_build_chunks_returns_empty_for_empty_directory(tmp_path):
    assert build_chunks(tmp_path) == []
