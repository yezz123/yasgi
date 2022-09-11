from requests import get

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_redirect():
    def app_wrapper():

        app = YASGI(content_type="application/json")

        @Routing("/target", content_type="text/plain")
        async def target_get(req, resp):
            return "TEXT_TARGET"

        @Routing("/redirect", content_type="text/plain")
        async def redirect(req, resp):
            await resp.redirect("/target")

        return app

    server = Server(app_wrapper)

    response = get("http://localhost:3000/redirect")
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.status_code in [200, 301]
    assert response.text == "TEXT_TARGET"

    server.stop()
