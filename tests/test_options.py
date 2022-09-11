from requests import get, options

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_options():
    def app_wrapper():
        app = YASGI(content_type="application/json", allow="*")

        @Routing("/options", methods=["GET", "POST", "HEAD"])
        async def opt(req, resp):
            return "OPTIONS RESPONSE"

        return app

    server = Server(app_wrapper)
    response = options("http://localhost:3000/options")
    assert response.headers["Access-Control-Allow-Methods"] == "GET,POST,HEAD"
    assert response.headers["Access-Control-Allow-Origin"] == "*"
    assert response.headers["Vary"] == "Access-Control-Request-Headers"
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == ""
    response = get("http://localhost:3000/options")
    assert response.headers["Content-Type"][:16] == "application/json"
    assert response.text == "OPTIONS RESPONSE"
    server.stop()
