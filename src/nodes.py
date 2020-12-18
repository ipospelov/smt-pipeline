from typing import Callable, Optional

from src.pipe import Pipe


class Node:
    def __init__(self, fun: Callable,
                 input_type: Optional[type] = None,
                 output_type: Optional[type] = None) -> None:
        self.fun = fun
        self.input_type = input_type
        self.output_type = output_type

        self.input_pipe = None
        self.output_pipe = None

    def set_pipes(self, input_pipe: Optional[Pipe] = None,
                  output_pipe: Optional[Pipe] = None) -> None:
        self.input_pipe = input_pipe
        self.output_pipe = output_pipe

    def do_work(self) -> None:
        # TODO: separate to Source, Sink subclasses
        if self.input_pipe:
            input_data = self.input_pipe.pop()

            if not input_data:
                return

            output_data = self.fun(*input_data)
        else:
            output_data = self.fun()

        if self.output_pipe:
            self.output_pipe.push((output_data,))
