# coding: utf-8

'''
Upstream latency reporter
==========================

This example allows you to collect upstream response time from nginx access log with the following log_format:

log_format with_latency '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        '"$http_x_forwarded_for" $upstream_response_time';
'''

import re
import sys
import time
import random
import datetime

from dotter import dotter


def main(path, size):
    publisher = dotter.Dotter.create(path, size)
    ts_current = time.time()
    values = [0]
    while True:
        line = sys.stdin.readline()
        timestamp, value = re.match(r'^.*\[(.*)\].* ([^ ]*)$', line).groups()
        timestamp = time.mktime(
            datetime.datetime.strptime(
                timestamp.split()[0], r'%d/%b/%Y:%H:%M:%S').utctimetuple())
        try:
            value = float(value)
        except ValueError:
            continue
        if timestamp == ts_current:
            values.append(value)
        else:
            publisher.dot(ts_current, sum(values) / len(values))
            ts_current = timestamp
            values = [value]


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
