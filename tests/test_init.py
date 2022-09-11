from re import compile

import pytest

from yasgi import YASGI, Routing


def test_init():
    test_app = YASGI()

    @Routing("/")
    async def root(req, resp):
        return None

    @Routing("/init-post", methods=["POST"])
    async def post(req, resp):
        return None

    @Routing("/get-post", methods=["GET", "POST"])
    async def get_post(req, resp):
        return None

    @Routing(compile("/getr.*"))
    async def get_r(req, resp):
        return None

    @Routing(compile("/getr.*"), methods=["POST"])
    async def get_rp(req, resp):
        return None

    @Routing(compile("/getr.*"), methods=["GET", "POST"])
    async def get_rgp(req, resp):
        return None
