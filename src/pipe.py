from collections import deque
from typing import Tuple, Optional


class Pipe:
    def __init__(self, data_type: type) -> None:
        self._buffer = deque()

        self.data_type = data_type

    def pop(self) -> Optional[Tuple]:
        if self._buffer:
            return self._buffer.pop()

    def push(self, data: Tuple) -> None:
        assert type(*data) is self.data_type

        self._buffer.append(data)
