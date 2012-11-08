import eventlet

from kzeventlet.pqueue import PeekableQueue

__threading = eventlet.import_patched('kazoo.handlers.threading')


class SequentialEventletHandler(__threading.SequentialThreadingHandler):
    sleep_func = staticmethod(eventlet.sleep)

    def peekable_queue(self, *args, **kwargs):
        return PeekableQueue(*args, **kwargs)
