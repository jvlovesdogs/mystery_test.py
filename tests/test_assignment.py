import pytest

from src.assignment import (
    Task,
    TaskScheduler,
    iou,
    parse_key_values,
    shortest_path_length,
    sliding_window_max,
)


def test_parse_key_values_basic():
    text = """
    host = example.com
    port= 443
    debug = true
    """
    assert parse_key_values(text) == {"host": "example.com", "port": "443", "debug": "true"}


def test_parse_key_values_comments_and_blanks():
    text = """
    # comment line
    a=1

    b = two  # trailing comment
    c= three
    """
    assert parse_key_values(text) == {"a": "1", "b": "two", "c": "three"}


def test_parse_key_values_invalid_line_raises():
    with pytest.raises(ValueError):
        parse_key_values("noequals")


def test_sliding_window_max_basic():
    assert sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]


def test_sliding_window_max_edges():
    assert sliding_window_max([2, 1], 1) == [2, 1]
    assert sliding_window_max([2, 1], 2) == [2]
    assert sliding_window_max([], 3) == []
    with pytest.raises(ValueError):
        sliding_window_max([1, 2, 3], 0)
    with pytest.raises(ValueError):
        sliding_window_max([1, 2, 3], 4)


def test_shortest_path_length_basic():
    # 0 = free, 1 = wall. 4-neighbor moves.
    grid = [
        [0, 0, 1],
        [1, 0, 1],
        [1, 0, 0],
    ]
    # shortest from (0,0) to (2,2) is length 4:
    # (0,0)->(0,1)->(1,1)->(2,1)->(2,2)
    assert shortest_path_length(grid) == 4


def test_shortest_path_length_blocked_or_empty():
    assert shortest_path_length([]) is None
    assert shortest_path_length([[]]) is None
    assert shortest_path_length([[1]]) is None
    assert shortest_path_length([[0]]) == 0


def test_shortest_path_length_non_rectangular_raises():
    with pytest.raises(ValueError):
        shortest_path_length([[0, 0], [0]])


def test_iou_basic_lists():
    a = [
        [1, 0],
        [1, 0],
    ]
    b = [
        [1, 1],
        [0, 0],
    ]
    # intersection = 1, union = 3
    assert iou(a, b) == pytest.approx(1 / 3)


def test_iou_all_zero():
    a = [[0, 0], [0, 0]]
    b = [[0, 0], [0, 0]]
    assert iou(a, b) == 1.0


def test_scheduler_valid_and_order():
    tasks = [
        Task("a", 3, ()),
        Task("b", 2, ("a",)),
        Task("c", 4, ("a",)),
        Task("d", 1, ("b", "c")),
    ]
    sch = TaskScheduler(tasks)
    assert sch.is_valid() is True

    order = sch.topological_order()
    # must contain all ids exactly once
    assert sorted(order) == ["a", "b", "c", "d"]
    # dependency constraints
    assert order.index("a") < order.index("b")
    assert order.index("a") < order.index("c")
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")


def test_scheduler_cycle_invalid():
    tasks = [
        Task("a", 1, ("b",)),
        Task("b", 1, ("a",)),
    ]
    sch = TaskScheduler(tasks)
    assert sch.is_valid() is False
    with pytest.raises(ValueError):
        sch.topological_order()
    with pytest.raises(ValueError):
        sch.critical_path_length()


def test_scheduler_unknown_dependency_invalid():
    tasks = [
        Task("a", 1, ("missing",)),
    ]
    sch = TaskScheduler(tasks)
    assert sch.is_valid() is False


def test_scheduler_critical_path():
    tasks = [
        Task("a", 3, ()),
        Task("b", 2, ("a",)),
        Task("c", 4, ("a",)),
        Task("d", 1, ("b", "c")),
    ]
    # critical path is a->c->d = 3+4+1 = 8
    sch = TaskScheduler(tasks)
    assert sch.critical_path_length() == 8
