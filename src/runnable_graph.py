from typing import List, Union

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

from src.nodes import Node
from src.pipe import Pipe


THREAD_POOL_SIZE = 4


class RunnableGraph:
    def __init__(self, structure: List[Union[type, Node]]) -> None:
        # TODO: pass graph structure to constructor, parse structure

        if not structure:
            return
        # проверяем, что типы на входах-выходах нод совпадают
        for index, item in enumerate(structure[:-1]):
            if item.output_type != structure[index + 1].input_type:
                return

        self.nodes = []
        for index, item in enumerate(structure):
            if item.output_type:  # output каналы создаются с первой ноды до предпоследней
                pipe_o = Pipe(item.output_type)

            node = item
            if index == 0:  # если это нода-источник, то у нее только канал на выход
                node.set_pipes(output_pipe=pipe_o)
            elif index == len(structure) - 1:  # если это последняя нода, то у нее только канал на вход
                node.set_pipes(input_pipe=pipe_i)
            else:  # если это обычная нода, то у нее и вход, и выход
                node.set_pipes(input_pipe=pipe_i, output_pipe=pipe_o)

            self.nodes.append(node)
            pipe_i = pipe_o # новый input pipe не создается, т.к. все input pipe это output pipe предыдущей ноды


        executors = {'default': ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)}
        # TODO: generate and add listeners for every node that produces a job execution
        self.scheduler = BackgroundScheduler(executors=executors)

    def run(self) -> None:
        self.scheduler.start()

        while True:
            for node in self.nodes:
                self.scheduler.add_job(func=node.do_work)
