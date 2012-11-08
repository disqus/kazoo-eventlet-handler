import eventlet
from pqueue import PeekableQueue

threading = eventlet.import_patched('kazoo.handlers.threading')

AsyncResult = threading.AsyncResult


class SequentialEventletHandler(threading.SequentialThreadingHandler):
    sleep_func = staticmethod(eventlet.sleep)

    def peekable_queue(self, *args, **kwargs):
        return PeekableQueue(*args, **kwargs)
