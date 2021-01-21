from enum import Enum


class Signal(int, Enum):
    STOP = 0
    CONTINUE = 1
