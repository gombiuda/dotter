# coding: utf-8

import sys
import time
import random

from . import dotter


def main(path, size):
    publisher = dotter.Dotter.create(path, size)
    value = 50
    while True:
        value -= random.random() - 0.5
        publisher.dot(time.time(), value)
        time.sleep(0.1)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
