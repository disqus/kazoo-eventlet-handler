import eventlet
from eventlet.hubs import get_hub
from eventlet.queue import _NONE, Empty, Queue, Waiter


class PeekableQueue(Queue):
    def get(self, *args, **kwargs):
        """
        Return and remove the first item from the queue.
        """
        return self.__call_when_item_available(self._get, *args, **kwargs)

    def peek(self, *args, **kwargs):
        """
        Return the first item in the queue, without removing it.
        """
        return self.__call_when_item_available(lambda: self.queue[0], *args, **kwargs)

    def __call_when_item_available(self, method, block=True, timeout=None):
        """
        Calls the given :param:`method` when an item is available.

        This provides the common implementation for fetching items from a
        non-empty queue that is used by both :meth:`get`` and :meth:`peek`.
        """
        # If the queue is not empty, we don't have to switch.
        if self.qsize():
            if self.putters:
                self._schedule_unlock()
            return method()

        # If this is a non-blocking read from the main loop, let the putters
        # run first before trying to fetch from the queue to increase the
        # likelihood that there actually is data.
        elif not block and get_hub().greenlet is eventlet.getcurrent():
            while self.putters:
                putter = self.putters.pop()
                if putter:
                    putter.switch(putter)
                    if self.qsize():
                        return method()

        # Wait until an item shows up in the queue to return, otherwise timeout.
        elif block:
            waiter = Waiter()
            timeout = eventlet.Timeout(timeout, Empty)
            try:
                self.getters.add(waiter)
                if self.putters:
                    self._schedule_unlock()

                # Wait until an item is added -- when one does, this greenlet
                # will be woken back up by :meth:`_unlock` and will resume here.
                result = waiter.wait()
                assert result is waiter, 'Invalid switch into Queue.__call_when_item_available: %r' % (result,)
                return method()
            finally:
                self.getters.discard(waiter)  # remove the waiter, no longer needed
                timeout.cancel()

        # No items, bail out now.
        else:
            raise Empty

    def _unlock(self):
        # Updated from :meth:`eventlet.queue.Queue` to allow ``getters`` to only
        # peek inside the queue, rather than always returning it.
        try:
            while True:
                if self.qsize() and self.getters:
                    getter = self.getters.pop()
                    if getter:
                        getter.switch(getter)
                elif self.putters and self.getters:
                    putter = self.putters.pop()
                    if putter:
                        getter = self.getters.pop()
                        if getter:
                            item = putter.item
                            putter.item = _NONE
                            self._put(item)
                            getter.switch(getter)
                            putter.switch(putter)
                        else:
                            self.putters.add(putter)
                elif self.putters and (self.getters or self.maxsize is None or self.qsize() < self.maxsize):
                    self.putters.pop().switch(putter)
                else:
                    break
        finally:
            self._event_unlock = None
