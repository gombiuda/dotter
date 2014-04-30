Dotter
=======

Dotter is a high performance module which allows your application to send data to the outside world without any dependency but a small file.

Here is how it works.

    +---------------+      +-------------------+
    |  Application  |      |     Displayer     |
    |               |      |                   |
    |  +---------+  |      |  +-------------+  |
    |  |Publisher|  |      |  |    Plot     |  |
    |  +---------+  |      |  +-------------+  |
    |      | |      |      |                   |
    +------|-|------+      +-------------------+
           | |                      ^
           \ /                     / \
            v                      | |
    +--------------+      +--------|-|--------+
    |  Filesystem  |      | Broker | |        |
    |              |      |        | |        |
    |  +--------+  |      |   +-----------+   |
    |  |  mmap  |--|------|-->| Collector |   |
    |  +--------+  |      |   +-----------+   |
    |              |      |                   |
    +--------------+      +-------------------+


Demo Time
----------

* Get ready

```
    $ pip install redis
```

* Start a Redis server to data storage


    $ redis-server &


* Start `Publisher`


    $ python -m dotter.publisher /tmp/data.mmap 1000 &


* Start `Borker` to transfer data to `Displayer`


    $ python -m dotter.broker /tmp/data.mmap 0.1 http://localhost:8000/data &


* Start `Collector` receive from `Broker`


    $ python app.py


* Go to `Displayer` to view time series


    $ open http://localhost:8000/static/index.html



Benchmark
-----------

`Dotter` basically won't affect the performance of your application.

It uses `mmap` to avoid network overhead, and also benefits from `mmap`'s lazy flush.

The following benchmark is run on my Macbook Pro Retina:

    $ python -m dotter.dotter benchmark ./dotter.mmap 10000
    Speed: 257752.541081 dots per second

And also run on a server with a normal disk:

    $ python -m dotter.dotter benchmark ./dotter.mmap 10000
    Speed: 158639.595752 dots per second

