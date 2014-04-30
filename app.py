# coding: utf-8

import os
import time
import json

import redis

from dotter import dotter

try:
    from igor import const
    redis_config = const.redis
except ImportError:
    redis_config = {'host': os.environ.get('REDIS_HOST', 'localhost'),
                    'port': os.environ.get('REDIS_PORT', 6379)}

rc = redis.StrictRedis(**redis_config)


def application(environ, start_response):
    global dot_series
    if environ['PATH_INFO'] == '/data':
        if environ['REQUEST_METHOD'] == 'GET':
            start_response('200 OK', [('Content-Type', 'application/json')])
            dots = rc.lrange('data', -500, -1)
            return [json.dumps([json.loads(dot) for dot in dots])]
        elif environ['REQUEST_METHOD'] == 'POST':
            length = int(environ['CONTENT_LENGTH'])
            dots = json.loads(environ['wsgi.input'].read(length))
            rc.rpush('data', *[json.dumps(dot) for dot in dots])
            if rc.llen('data') > 500:
                rc.lpop('data')
            start_response('200 OK', [])
            return []
        else:
            start_response('400 Bad Request', [])
            return []
    else:
        start_response('200 OK', [])
        with open(environ['PATH_INFO'].strip('/')) as f:
            return [f.read()]

def main():
    from wsgiref.simple_server import make_server
    http = make_server('', 8000, application)
    print 'Server started'
    http.serve_forever()


if __name__ == '__main__':
    main()
