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
        if type(data) is not self.data_type:
            raise TypeError

        self._buffer.append(data)

    def is_empty(self) -> bool:
        return not bool(self._buffer)
