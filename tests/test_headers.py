from requests import get

from tests.conftest import Server
from yasgi import YASGI, Routing


def test_headers():
    def app_wrapper():
        app = YASGI(content_type="application/json")

        @Routing("/header", content_type="text/plain")
        async def header(req, resp):
            resp.add_header("test", "12345")
            return ""

        @Routing("/header-req", content_type="text/plain")
        async def header_req(req, resp):
            header = req.headers.get("jezevec")
            return f"header={str(header)}"

        return app

    server = Server(app_wrapper)
    response = get("http://localhost:3000/header")
    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == ""
    assert response.headers["test"] == "12345"
    response = get("http://localhost:3000/header-req", headers={"jezevec": "pes"})
    assert response.status_code == 200
    assert response.headers["Content-Type"][:10] == "text/plain"
    assert response.text == "header=pes"
    server.stop()
