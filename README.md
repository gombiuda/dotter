Dotter
=======

Dotter是一个高性能打点模块，能够在不影响原有程序性能的情况下，输出时间序列数据，并实时绘出该时间序列，以便动态观察程序的运行状态。


准备
-------

    $ pip install requests redis
    $ redis-server


启动数据生成模块
-------------

    $ python -m dotter.publisher data.mmap 1000


启动实时绘图模块
-------------

    $ python app.py


启动数据收集模块
-------------

    $ python -m dotter.broker data.mmap 0.1 http://localhost:8000/data


观察数据
----------

    $ open http://localhost:8000/static/index.html


TODO
-------

* 显示更多历史数据
