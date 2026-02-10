from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


def parse_key_values(text: str) -> Dict[str, str]:
    """
    TODO
    """
    raise NotImplementedError


def sliding_window_max(values: Sequence[int], k: int) -> List[int]:
    """
    TODO
    """
    raise NotImplementedError


def shortest_path_length(grid: Sequence[Sequence[int]]) -> Optional[int]:
    """
    TODO
    """
    raise NotImplementedError


def iou(mask_a, mask_b) -> float:
    """
    TODO: mask_a and mask_b may be list of lists of 0/1 or numpy arrays.
    """
    raise NotImplementedError


@dataclass(frozen=True)
class Task:
    id: str
    duration: int
    deps: Tuple[str, ...]


class TaskScheduler:
    """
    TODO: schedule tasks with dependencies.
    """

    def __init__(self, tasks: Iterable[Task]) -> None:
        raise NotImplementedError

    def is_valid(self) -> bool:
        raise NotImplementedError

    def topological_order(self) -> List[str]:
        raise NotImplementedError

    def critical_path_length(self) -> int:
        raise NotImplementedError
