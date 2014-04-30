# coding: utf-8

import os
import sys
import time
import struct
import unittest

class Dotter(object):
    def __init__(self, path):
        import mmap
        self.fd = open(path, 'rb+')
        if os.stat(path).st_size % 16 != 0:
            raise ValueError('mmap size invalid')
        self.size = (os.stat(path).st_size - 16) / 16
        self.trunk = mmap.mmap(self.fd.fileno(), 0)

    @staticmethod
    def create(path, size):
        with open(path, 'wb') as f:
            f.seek(16 + 16 * size - 1)
            f.write('\0')
        return Dotter(path)

    def dot(self, timestamp, value):
        self.trunk.seek(0)
        pos_w, = struct.unpack('Q', self.trunk.read(8))
        self.trunk.seek(8)
        pos_r, = struct.unpack('Q', self.trunk.read(8))
        if pos_w > pos_r and pos_w % self.size == pos_r % self.size:
            pos_w -= 1
        self.trunk.seek(16 + (pos_w % self.size) * 16)
        self.trunk.write(struct.pack('dd', float(timestamp), float(value)))
        self.trunk.seek(0)
        self.trunk.write(struct.pack('Q', pos_w + 1))

    def close(self):
        self.trunk.close()
        self.fd.close()

    def destroy(self):
        os.remove(self.path)


class Broker(object):
    def __init__(self, path):
        import mmap
        self.fd = open(path, 'rb+')
        if os.stat(path).st_size % 16 != 0:
            raise ValueError('mmap size invalid')
        self.size = (os.stat(path).st_size - 16) / 16
        self.trunk = mmap.mmap(self.fd.fileno(), 0)

    def read(self, n=0):
        self.trunk.seek(0)
        pos_w, = struct.unpack('Q', self.trunk.read(8))
        self.trunk.seek(8)
        pos_r, = struct.unpack('Q', self.trunk.read(8))
        if n == 0:
            n = pos_w - pos_r - 1
        dots = []
        for i in range(n):
            self.trunk.seek(16 + ((pos_r + i) % self.size) * 16)
            data = self.trunk.read(16)
            if len(data) != 16:
                raise ValueError('data invalid %r' % data)
            else:
                dots.append(struct.unpack('dd', data))
        self.trunk.seek(8)
        self.trunk.write(struct.pack('Q', pos_r + n))
        return dots


def benchmark(path, size):
    import random
    dotter = Dotter.create(path, size)

    count = 0
    start = time.time()
    while True:
        dotter.dot(time.time(), random.random())
        count += 1
        if count % 10000 == 0:
            print 'Speed: %s dots per second' % (1 / (time.time() - start) * 10000)
            count = 0
            start = time.time()


class DotterTestCase(unittest.TestCase):
    def setUp(self):
        self.dotter = Dotter.create('/tmp/foo.mmap', 100)
        self.broker = Broker('/tmp/foo.mmap')

    def tearDown(self):
        os.remove('/tmp/foo.mmap')

    def test_read_1(self):
        dots = []
        for i in range(50):
            dots.append((time.time(), float(i)))
            self.dotter.dot(dots[i][0], dots[i][1])
        for i in range(50):
            dot = self.broker.read(1)[0]
            self.assertEqual(dot, dots[i])

    def test_read_n(self):
        dots = []
        for i in range(50):
            dots.append((time.time(), float(i)))
            self.dotter.dot(dots[i][0], dots[i][1])
        for i in range(5):
            self.assertEqual(self.broker.read(10), dots[i * 10:(i + 1) * 10])

    def test_read_much(self):
        for i in range(10000):
            dot = (time.time(), float(i))
            self.dotter.dot(dot[0], dot[1])
            self.assertEqual(dot, self.broker.read(1)[0])


if __name__ == '__main__':
    if sys.argv[1] == 'test':
        unittest.main(argv=[sys.argv[0]])
    elif sys.argv[1] == 'benchmark':
        benchmark(sys.argv[2], int(sys.argv[3]))
        time.sleep(1)
