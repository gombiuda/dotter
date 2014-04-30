# coding: utf-8

import sys
import time
import json
import urllib2

from . import dotter


def main(path, poll, remote):
    subscriber = dotter.Broker(path)
    while True:
        dots = subscriber.read()
        try:
            response = urllib2.urlopen(remote, json.dumps(dots))
        except Exception:
            pass
        time.sleep(poll)


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3])
