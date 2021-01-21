from collections import deque
from typing import Tuple, Optional


class Pipe:
    def __init__(self, data_type: type) -> None:
        self._buffer = deque()
        self._event_buffer = deque()

        self.data_type = data_type
        self._data_expired = False

    def pop(self) -> Optional[Tuple]:
        if self._buffer:
            return self._buffer.pop()

    def push(self, data: Tuple) -> None:
        if type(data) is not self.data_type:
            raise TypeError(f'Expected: {self.data_type}, got: {type(data)}, value: {data}')

        self._buffer.append(data)

    def set_expired(self) -> None:
        self._data_expired = True

    def is_expired(self) -> bool:
        return self._data_expired

    def is_empty(self) -> bool:
        return not bool(self._buffer)
