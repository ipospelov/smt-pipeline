import os
import sys
from time import sleep

import cv2
import numpy as np

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


input_folder = '/Users/ivanpospelov/Study/pipeline/tmp/input_images'
generator = (filename for filename in os.listdir(input_folder))


def read_image_fun():
    try:
        filename = next(generator)
        return cv2.imread(os.path.join(input_folder, filename))
    except:
        return None


input_folder_2 = '/Users/ivanpospelov/Study/pipeline/tmp/input_images_2'
generator_2 = (filename for filename in os.listdir(input_folder_2))


def read_image_fun_2():
    try:
        filename = next(generator_2)
        return cv2.imread(os.path.join(input_folder_2, filename))
    except:
        return None


def blur_fun(img):
    return cv2.blur(img, (10, 10))


filenames = (f'{i}.jpg' for i in range(sys.maxsize ** 10))


def write_image_fun(img):
    cv2.imwrite(next(filenames), img)


def double_exposure_fun(img1, img2):
    img1 = np.float32(cv2.resize(img1, (600, 400)))
    img2 = np.float32(cv2.resize(img2, (600, 400)))
    return (img1 + img2) * 0.5


def sharpen_fun(img):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(img, -1, kernel)


def rotate_image(img):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, 45, 1.0)
    return cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)


def run_numerical_graph():
    source = Node(read_image_fun, output_type=int, is_source=True)
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

    sleep(10)


if __name__ == '__main__':
    source_cat = Node(read_image_fun, output_type=np.ndarray, is_source=True)
    source_dog = Node(read_image_fun_2, output_type=np.ndarray, is_source=True)

    sharpen_node = Node(sharpen_fun, input_type=np.ndarray, output_type=np.ndarray)
    blur_node = Node(blur_fun, input_type=np.ndarray, output_type=np.ndarray)

    merge_node = Node(double_exposure_fun, input_type=tuple, output_type=np.ndarray)
    rotate_node = Node(rotate_image, input_type=np.ndarray, output_type=np.ndarray)

    write_node = Node(write_image_fun, input_type=np.ndarray)

    graph = RunnableGraph(is_blocking=True)

    graph.link_nodes(source_cat, sharpen_node)
    graph.link_nodes(sharpen_node, merge_node)
    graph.link_nodes(merge_node, rotate_node)
    graph.link_nodes(rotate_node, write_node)
    graph.link_nodes(source_dog, blur_node)
    graph.link_nodes(blur_node, merge_node)

    graph.run()
