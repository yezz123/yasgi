from json import loads
from re import compile

from requests import get

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_get():
    def app_wrapper():
        app = YASGI(content_type="application/json")

        @Routing("/", content_type="text/plain")
        async def root_get(req, resp):
            return "TEXT_RESPONSE_FROM_ROOT"

        @Routing("/json")
        async def json_get(req, resp):
            return {"reponse": "json-response"}

        @Routing("/query-params")
        async def query_param_get(req, resp):
            return {"query_params": req.query_params}

        @Routing(compile("/text.+"), content_type="text/plain")
        async def regex(req, resp):
            return "text jak hovado"

        @Routing(compile("/param-(.*)"))
        async def rege_param(req, resp, param):
            return {"param": param}

        return app

    server = Server(app_wrapper)
    response = get("http://localhost:3000")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == "TEXT_RESPONSE_FROM_ROOT"
    response = get("http://localhost:3000/json/")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:16] == "application/json"
    assert loads(response.text) == {"reponse": "json-response"}
    response = get("http://localhost:3000/query-params?jezevec=pes")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:16] == "application/json"
    assert loads(response.text) == {"query_params": {"jezevec": "pes"}}
    response = get("http://localhost:3000/text-")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == "text jak hovado"
    response = get("http://localhost:3000/text")
    assert response.status_code == 404
    response = get("http://localhost:3000/param-jezevec")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:16] == "application/json"
    assert loads(response.text) == {"param": "jezevec"}
    server.stop()
