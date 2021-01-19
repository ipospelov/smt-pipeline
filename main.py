from time import sleep

from src.nodes import Node
from src.runnable_graph import RunnableGraph


def source_fun():
    return 1


def sum_fun(a):
    return a + 1


def multiple_fun(a):
    return a * 2


def power_fun(a):
    return a ** 3


def sink_fun(*args):
    print(args)


if __name__ == '__main__':
    source = Node(source_fun, output_type=int, is_source=True)
    left = Node(sum_fun, input_type=int, output_type=int)
    right0 = Node(sum_fun, input_type=int, output_type=int)
    right1 = Node(multiple_fun, input_type=int, output_type=int)
    right1_duplicate = Node(power_fun, input_type=int, output_type=int)
    sink = Node(sink_fun, input_type=tuple)

    graph = RunnableGraph()

    graph.link_nodes(source, left)
    graph.link_nodes(source, right0)
    graph.link_nodes(right0, right1)
    graph.link_nodes(right0, right1_duplicate)
    graph.link_nodes(left, sink)
    graph.link_nodes(right1, sink)
    graph.link_nodes(right1_duplicate, sink)

    graph.run()

    sleep(100)
