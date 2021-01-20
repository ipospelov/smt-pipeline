from typing import Callable, Optional, List


class Node:
    def __init__(self, fun: Callable,
                 input_type: Optional[type] = None,
                 output_type: Optional[type] = None,
                 is_source: bool = False) -> None:
        self.fun = fun
        self.input_type = input_type
        self.output_type = output_type
        self.is_source = is_source
        self.subscribed_nodes = is_source and [self] or []

        self.input_pipes = []
        self.output_pipes = []

    def append_subscriber(self, subscriber) -> None:
        self.subscribed_nodes.append(subscriber)

    def append_input_pipe(self, pipe) -> None:
        self.input_pipes.append(pipe)

    def append_output_pipe(self, pipe) -> None:
        self.output_pipes.append(pipe)

    def do_work(self) -> Optional[List]:
        if self.input_pipes:
            if any(pipe.is_empty() for pipe in self.input_pipes):
                return

            input_data = tuple(pipe.pop() for pipe in self.input_pipes)

            if not input_data or len(input_data) != len(self.input_pipes):
                return

            output_data = self.fun(*input_data)
        else:
            output_data = self.fun()

        if output_data is None:
            return

        for output_pipe in self.output_pipes:
            output_pipe.push(output_data)

        return self.subscribed_nodes
