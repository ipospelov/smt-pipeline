from enum import Enum


class NodeType(int, Enum):
    BASE = 0
    SOURCE = 1
    SINK = 2
