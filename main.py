from time import sleep

from src.nodes import Node
from src.runnable_graph import RunnableGraph


def source_fun():
    return 1


def sum_fun(a):
    return a + 1


def sink_fun(a):
    print(a)


if __name__ == '__main__':
    graph_structure = [
        Node(source_fun, output_type=int),
        Node(sum_fun, input_type=int, output_type=int),
        Node(sink_fun, input_type=int)
    ]
    graph = RunnableGraph(graph_structure)
    graph.run()

    sleep(1)
