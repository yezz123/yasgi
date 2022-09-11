import contextlib

from yasgi.exceptions import InputParseError
from yasgi.requests import HTTPRequest, Request
from yasgi.responses import HTTPAbort, HTTPResponse, Response
from yasgi.routing import HTTPRouting, WebsocketsRouting


class YASGI:
    """
    ASGI is a class that is used to create an ASGI application.

    ASGI is asynchronous callable, that is it accepts scope which contains information about incoming request,
    send, an awaitable that lets you send events to the client, and receive, an awaitable which lets you receive events from the client.

    :param content_type: The content_type of the application.
    :param charset: The charset of the application.
    :param allow: The allowed methods of the application.
    """

    __slots__ = ()
    _content_type = ""
    _charset = ""
    _allow = None
    triggers: dict = {}

    def __init__(
        self, content_type: str = "application/json", charset: str = "UTF-8", allow=""
    ):
        YASGI._content_type = content_type
        YASGI._charset = charset
        YASGI._allow = allow

    @staticmethod
    async def __call__(scope, receive, send):
        event = await receive()
        if scope["type"] == "http":
            while event["more_body"]:
                more = await receive()
                event["body"] += more["body"]
                event["more_body"] = more["more_body"]
            await YASGI._http(scope, event, send)
        elif event["type"] == "websocket.connect":
            await YASGI._websockets(scope, send, receive)

    @staticmethod
    async def _http(scope, event, send):
        method, url_args, not_allowed, ct = HTTPRouting.get(
            scope["path"], scope["method"]
        )

        request = HTTPRequest(scope, event)
        response = HTTPResponse(
            send,
            content_type=ct or YASGI._content_type,
            charset=YASGI._charset,
            allow=YASGI._allow,
        )

        with contextlib.suppress(HTTPAbort):
            if not_allowed:
                await response.abort(status=405)
            elif not method:
                await response.abort(status=404)
            try:
                body = await method(request, response, *url_args)
            except InputParseError:
                await response.abort(status=400)
            if not response.processed:
                await response.process(body)

    @staticmethod
    async def _websockets(scope, send, receive):
        trigger, url_args, ct = WebsocketsRouting.get(scope["path"])
        if trigger:
            await send({"type": "websocket.accept"})
            while True:
                event = await receive()
                request = Request(scope, event, content_type=YASGI._content_type)
                response = Response(
                    send, content_type=ct or YASGI._content_type, charset=YASGI._charset
                )
                try:
                    await trigger(request, response, url_args)
                except InputParseError:
                    response.send(
                        {
                            "status": False,
                            "error": "P001",
                            "message": "Data JSON parse error",
                        }
                    )
                if event["type"] == "websocket.disconnect":
                    break
        else:
            await send({"type": "websocket.close"})
