import unittest

import eventlet
import mock
from kazoo.client import KazooClient
__client_tests = eventlet.import_patched('kazoo.tests.test_client')

from kzeventlet.handler import SequentialEventletHandler


class EventletKazooClient(KazooClient):
    """
    A KazooClient that is bound to using the eventlet handler.
    """
    def setUp(self, *args, **kwargs):
        kwargs['handler'] = SequentialEventletHandler()
        return super(EventletKazooClient, self).super(*args, **kwargs)


class EventletTestCaseMixin(object):
    """
    A mixin for Kazoo test cases that forces the test runner to only use the
    client with SequentialEventletHandler.
    """
    @mock.patch('kazoo.client.KazooClient')
    def expire_session(self, mock_client, *args, **kwargs):
        # Force using the :class:`SequentialEventletHandler` instead of threaded,
        # this method doesn't actually call :meth:`_get_client`.
        mock_client.return_value = SequentialEventletHandler.__init__
        return super(EventletTestCaseMixin, self).expire_session(*args, **kwargs)

    def _get_client(self, **kwargs):
        kwargs['handler'] = SequentialEventletHandler()
        return super(EventletTestCaseMixin, self)._get_client(**kwargs)


class TestConnection(EventletTestCaseMixin, __client_tests.TestConnection):
    pass


class TestClient(EventletTestCaseMixin, __client_tests.TestClient):
    pass
