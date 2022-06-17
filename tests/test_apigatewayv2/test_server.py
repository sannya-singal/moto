import json
import sure  # noqa # pylint: disable=unused-import

import moto.server as server
from tests import DEFAULT_ACCOUNT_ID


def test_apigatewayv2_list_apis():
    backend = server.create_backend_app(
        account_id=DEFAULT_ACCOUNT_ID, service="apigatewayv2"
    )
    test_client = backend.test_client()

    resp = test_client.get("/v2/apis")
    resp.status_code.should.equal(200)
    json.loads(resp.data).should.equal({"items": []})
