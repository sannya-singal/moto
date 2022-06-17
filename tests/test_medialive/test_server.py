import sure  # noqa # pylint: disable=unused-import

import moto.server as server
from moto import mock_medialive
from tests import DEFAULT_ACCOUNT_ID

"""
Test the different server responses
"""


@mock_medialive
def test_medialive_list_channels():
    backend = server.create_backend_app(
        account_id=DEFAULT_ACCOUNT_ID, service="medialive"
    )
    test_client = backend.test_client()

    res = test_client.get("/prod/channels")
    result = res.data.decode("utf-8")
    result.should.contain('"channels": []')


@mock_medialive
def test_medialive_list_inputs():
    backend = server.create_backend_app(
        account_id=DEFAULT_ACCOUNT_ID, service="medialive"
    )
    test_client = backend.test_client()

    res = test_client.get("/prod/inputs")

    result = res.data.decode("utf-8")
    result.should.contain('"inputs": []')
