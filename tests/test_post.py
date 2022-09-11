from json import loads

from requests import post, put

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_post():
    def app_wrapper():
        app = YASGI(content_type="application/json")

        @Routing("/post", methods=["POST"])
        async def post(req, resp):
            return req.data

        @Routing("/put", methods=["PUT"])
        async def put(req, resp):
            return req.data

        return app

    server = Server(app_wrapper)

    response = post("http://localhost:3000/post", json={"input": "test-post"})
    assert response.status_code == 200
    assert response.headers["Content-Type"][:16] == "application/json"
    assert loads(response.text) == {"input": "test-post"}

    response = put("http://localhost:3000/put", json={"input": "test-put"})
    assert response.status_code == 200
    assert response.headers["Content-Type"][:16] == "application/json"
    assert loads(response.text) == {"input": "test-put"}

    server.stop()
