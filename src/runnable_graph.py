from typing import List, Union

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler

from src.nodes import Node
from src.pipe import Pipe


THREAD_POOL_SIZE = 4


class RunnableGraph:
    def __init__(self, is_blocking=False) -> None:
        self.nodes = []

        executors = {'default': ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)}

        if is_blocking:
            self.scheduler = BlockingScheduler(executors=executors)
        else:
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

        def log(event):
            print('Exception raised: ', event)

        self.scheduler.add_listener(node_listener, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(log, EVENT_JOB_ERROR)

    def run(self) -> None:
        sources = {node for node in self.nodes if node.is_source}

        for node in sources:
            self.scheduler.add_job(func=node.do_work)

        self.scheduler.start()
