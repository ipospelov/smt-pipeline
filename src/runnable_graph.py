from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from src.nodes import Node
from src.pipe import Pipe


def source_fun():
    return 1


def sum_fun(a):
    return a + 1


def sink_fun(a):
    print(a)


THREAD_POOL_SIZE = 4


class RunnableGraph:
    def __init__(self) -> None:
        # TODO: pass graph structure to constructor, parse structure
        source_output_pipe = Pipe()
        source = Node(source_fun, output_pipe=source_output_pipe)

        node_output_pipe = Pipe()
        node = Node(sum_fun, input_pipe=source_output_pipe, output_pipe=node_output_pipe)

        sink = Node(sink_fun, input_pipe=node_output_pipe)

        self.nodes = [source, node, sink]
        executors = {'default': ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)}

        # TODO: generate and add listeners for every node that produces a job execution
        self.scheduler = BackgroundScheduler(executors=executors)

    def run(self) -> None:
        self.scheduler.start()

        for i in range(3):
            for node in self.nodes:
                self.scheduler.add_job(func=node.do_work)
