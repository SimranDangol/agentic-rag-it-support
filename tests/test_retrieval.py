from app.retrieval import rrf


def test_rrf_prefers_items_in_both_lists():
    merged = rrf([["a", "b", "c"], ["c", "a", "d"]])
    assert merged[0] == "a", "Item in both lists at top rank should score highest"
    assert set(merged) == {"a", "b", "c", "d"}, "All items should appear in output"


def test_rrf_single_list():
    merged = rrf([["x", "y", "z"]])
    assert merged == ["x", "y", "z"]


def test_rrf_empty():
    assert rrf([]) == []
