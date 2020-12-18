from typing import List, Union

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from src.nodes import Node
from src.pipe import Pipe


THREAD_POOL_SIZE = 4


class RunnableGraph:
    def __init__(self, structure: List[Union[type, Node]]) -> None:
        # TODO: pass graph structure to constructor, parse structure

        # if not structure:
        #     return
        #
        # for index, item in enumerate(structure[:-1]):

        source = structure[0]
        source_output_pipe = Pipe(source.output_type)

        node = structure[1]
        node_output_pipe = Pipe(node.output_type)

        sink = structure[2]

        source.set_pipes(output_pipe=source_output_pipe)
        node.set_pipes(input_pipe=source_output_pipe, output_pipe=node_output_pipe)
        sink.set_pipes(input_pipe=node_output_pipe)

        self.nodes = [source, node, sink]

        executors = {'default': ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)}
        # TODO: generate and add listeners for every node that produces a job execution
        self.scheduler = BackgroundScheduler(executors=executors)

    def run(self) -> None:
        self.scheduler.start()

        while True:
            for node in self.nodes:
                self.scheduler.add_job(func=node.do_work)
