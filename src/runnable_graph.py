from typing import List, Union

from apscheduler.events import EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from src.nodes import Node
from src.pipe import Pipe


THREAD_POOL_SIZE = 4


class RunnableGraph:
    def __init__(self) -> None:
        self.nodes = []

        executors = {'default': ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)}
        self.scheduler = BackgroundScheduler(executors=executors)

        self._produce_listeners()

    def link_nodes(self, source: Node, target: Node) -> None:
        pipe = Pipe(source.output_type)

        source.append_output_pipe(pipe)
        target.append_input_pipe(pipe)

        source.append_subscriber(target)

        self.nodes.extend([source, target])

    def _produce_listeners(self):
        def node_listener(event):
            subscribers = event.retval
            if not subscribers:
                return

            for node in subscribers:
                self.scheduler.add_job(func=node.do_work)

        self.scheduler.add_listener(node_listener, EVENT_JOB_EXECUTED)

    def run(self) -> None:
        self.scheduler.start()

        sources = {node for node in self.nodes if node.is_source}

        for node in sources:
            self.scheduler.add_job(func=node.do_work)
