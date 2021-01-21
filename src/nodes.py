from typing import Callable, Optional, List, Tuple

from src.exceptions import SinkExpiredException
from src.node_types import NodeType
from src.signals import Signal


class Node:
    def __init__(self, fun: Callable,
                 input_type: Optional[type] = None,
                 output_type: Optional[type] = None,
                 node_type: NodeType = NodeType.BASE) -> None:
        self.fun = fun
        self.input_type = input_type
        self.output_type = output_type
        self.node_type = node_type
        self.subscribed_nodes = self.is_source and [self] or []

        self.input_pipes = []
        self.output_pipes = []

    @property
    def is_source(self) -> bool:
        return self.node_type == NodeType.SOURCE

    @property
    def is_sink(self) -> bool:
        return self.node_type == NodeType.SINK

    def append_subscriber(self, subscriber) -> None:
        self.subscribed_nodes.append(subscriber)

    def append_input_pipe(self, pipe) -> None:
        self.input_pipes.append(pipe)

    def append_output_pipe(self, pipe) -> None:
        self.output_pipes.append(pipe)

    def _propagate_expired(self) -> None:
        for output_pipe in self.output_pipes:
            output_pipe.set_expired()

    def do_work(self) -> Optional[Tuple]:
        if self.input_pipes:
            if any(pipe.is_empty() for pipe in self.input_pipes):
                return None, None, None

            input_data = tuple(pipe.pop() for pipe in self.input_pipes)

            output_data = self.fun(*input_data)
        else:
            output_data = self.fun()

        if output_data is None:
            self._propagate_expired()
            return None, None, None

        for output_pipe in self.output_pipes:
            output_pipe.push(output_data)

        retval_signal = Signal.CONTINUE
        input_expired = all(pipe.is_empty() and pipe.is_expired()
                            for pipe in self.input_pipes)
        if input_expired:
            self._propagate_expired()
            if self.is_sink:
                retval_signal = Signal.STOP

        return retval_signal, self, self.subscribed_nodes
