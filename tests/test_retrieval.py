from app import retrieval
from app.retrieval import expand_adjacent_chunks, rrf


def test_rrf_prefers_items_in_both_lists():
    merged = rrf([["a", "b", "c"], ["c", "a", "d"]])
    assert merged[0] == "a", "Item in both lists at top rank should score highest"
    assert set(merged) == {"a", "b", "c", "d"}, "All items should appear in output"


def test_rrf_single_list():
    merged = rrf([["x", "y", "z"]])
    assert merged == ["x", "y", "z"]


def test_rrf_empty():
    assert rrf([]) == []


def test_expand_adjacent_chunks_includes_neighbors_from_same_source(monkeypatch):
    chunks = {
        f"guide.md-{i}": {"id": f"guide.md-{i}", "source": "guide.md", "text": str(i)}
        for i in range(3)
    }
    monkeypatch.setattr(retrieval, "BY_ID", chunks)

    expanded = expand_adjacent_chunks([chunks["guide.md-1"]])

    assert [chunk["id"] for chunk in expanded] == [
        "guide.md-0",
        "guide.md-1",
        "guide.md-2",
    ]
