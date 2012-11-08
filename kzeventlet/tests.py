import unittest

import eventlet
import mock
from kazoo.client import KazooClient
__client_tests = eventlet.import_patched('kazoo.tests.test_client')

from kzeventlet.handler import SequentialEventletHandler


class EventletKazooClient(KazooClient):
    def setUp(self, *args, **kwargs):
        kwargs['handler'] = SequentialEventletHandler()
        return super(EventletKazooClient, self).super(*args, **kwargs)


class EventletTestCaseMixin(object):
    @mock.patch('kazoo.client.KazooClient')
    def expire_session(self, mock_client, *args, **kwargs):
        mock_client.return_value = SequentialEventletHandler.__init__
        return super(EventletTestCaseMixin, self).expire_session(*args, **kwargs)

    def _get_client(self, **kwargs):
        kwargs['handler'] = SequentialEventletHandler()
        return super(EventletTestCaseMixin, self)._get_client(**kwargs)


class TestConnection(EventletTestCaseMixin, __client_tests.TestConnection):
    pass


class TestClient(EventletTestCaseMixin, __client_tests.TestClient):
    pass
