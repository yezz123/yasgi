from requests import get

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_cookies():
    def app_wrapper():
        app = YASGI(content_type="application/json")

        @Routing("/cookie", content_type="text/plain")
        async def header(req, resp):
            resp.set_cookie("test-cookie", "12345-cookie")
            return ""

        @Routing("/cookie-req", content_type="text/plain")
        async def header_req(req, resp):
            jezevec = req.cookies["jezevec"]
            return "{}-{}".format(jezevec.value, jezevec["max-age"])

        return app

    server = Server(app_wrapper)
    response = get("http://localhost:3000/cookie")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == ""
    assert response.cookies["test-cookie"] == "12345-cookie"
    response = get(
        "http://localhost:3000/cookie-req",
        headers={"Cookie": "jezevec=kocka; Max-Age=345"},
    )

    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == "kocka-345"
    server.stop()
