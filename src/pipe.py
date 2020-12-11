from collections import deque
from typing import Tuple, Optional


class Pipe:
    def __init__(self) -> None:
        self._buffer = deque()

    def pop(self) -> Optional[Tuple]:
        if self._buffer:
            return self._buffer.pop()

    def push(self, data: Tuple) -> None:
        self._buffer.append(data)
