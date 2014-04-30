# coding: utf-8

import sys
import time
import json

import requests

from . import dotter


def main(path, poll, remote):
    subscriber = dotter.Broker(path)
    while True:
        dots = subscriber.read()
        response = requests.post(remote, json.dumps(dots))
        time.sleep(poll)


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3])
