import json
import sure  # noqa # pylint: disable=unused-import

import moto.server as server
from moto import mock_kms
from tests import DEFAULT_ACCOUNT_ID

"""
Test the different server responses
"""


@mock_kms
def test_list_keys():
    backend = server.create_backend_app(account_id=DEFAULT_ACCOUNT_ID, service="kms")
    test_client = backend.test_client()

    res = test_client.get("/?Action=ListKeys")

    json.loads(res.data.decode("utf-8")).should.equal(
        {"Keys": [], "NextMarker": None, "Truncated": False}
    )
