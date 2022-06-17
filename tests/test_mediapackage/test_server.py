import sure  # noqa # pylint: disable=unused-import

import moto.server as server
from moto import mock_mediapackage
from tests import DEFAULT_ACCOUNT_ID

"""
Test the different server responses
"""


@mock_mediapackage
def test_mediapackage_list_channels():
    backend = server.create_backend_app(
        account_id=DEFAULT_ACCOUNT_ID, service="mediapackage"
    )
    test_client = backend.test_client()

    res = test_client.get("/channels")
    result = res.data.decode("utf-8")
    result.should.contain('"channels": []')


@mock_mediapackage
def test_mediapackage_list_origin_endpoints():
    backend = server.create_backend_app(
        account_id=DEFAULT_ACCOUNT_ID, service="mediapackage"
    )
    test_client = backend.test_client()

    res = test_client.get("/origin_endpoints")
    result = res.data.decode("utf-8")
    result.should.contain('"originEndpoints": []')
