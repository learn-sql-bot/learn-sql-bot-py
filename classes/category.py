from dataclasses import dataclass, field
from typing import List
from classes.exercise import Exercise


@dataclass
class Category:
    """ Информация об упражнении"""

    id: int
    code: str
    title: str
    order: int
    exercises: List[Exercise] = field(default_factory=list)


