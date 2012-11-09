kazoo-eventlet-handler
======================

A Kazoo handler for usage in eventlet greenthreaded environments.

Usage
-----

.. code:: python

    from kazoo.client import KazooClient
    from kzeventlet.handler import SequentialEventletHandler

    zookeeper = KazooClient(handler=SequentialEventletHandler())
