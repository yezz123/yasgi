from re import Pattern


class Routing:
    """
    Routing class for HTTP requests and Websockets, this class is used to create a routing object.

    Routing is asynchronous callable, that is it accepts scope which contains information about incoming request,
    send, an awaitable that lets you send events to the client, and receive, an awaitable which lets you receive events from the client.

    :param args: Arguments for routing.
    :param type: Type of routing.
    """

    __slots__ = "_instance"

    def __init__(self, *args, type: str = "http", **kwargs):
        if type.lower() == "http":
            self._instance = HTTPRouting(*args, **kwargs)
        elif type.lower() == "websocket":
            self._instance = WebsocketsRouting(*args, **kwargs)

    def __call__(self, call, *args):
        return self._instance(call, *args)


class WebsocketsRouting:
    """
    The WebSocket API is an advanced technology that makes it possible to open a two-way interactive communication session between the user's browser and a server. With this API, you can send messages to a server and receive event-driven responses without having to poll the server for a reply.

    :param route: The route to the function.
    :param content_type: The content type of the request.
    """

    __slots__ = ("_route", "_content_type")
    __routes: dict = {}
    __regex_routes: list = []

    def __init__(self, route, content_type=None):
        self._content_type = content_type
        if type(route) == str:
            if route[0] != "/":
                raise RuntimeError("Router must start with '/'! (%s)" % route)
            self._route = route if route[-1] == "/" else f"{route}/"
        elif type(route) == Pattern:
            self._route = route
        else:
            raise RuntimeError(
                f"Router must be str or re.Pattern type! ({route}, {str(type(route))})"
            )

    def __call__(self, fce, *args):
        if type(self._route) == Pattern:
            self.__regex_routes.append((self._route, fce, self._content_type))
        elif self._route in self.__routes:
            raise RuntimeError(f"Route alreay set! ({self._route})")
        else:
            self.__routes[self._route] = fce, self._content_type
        return fce

    @staticmethod
    def get(path: str) -> tuple:
        route = WebsocketsRouting.__routes.get(
            path if path[-1] == "/" else f"{path}/", {}
        )
        if route:
            return route[0], None, route[1]
        for item in WebsocketsRouting.__regex_routes:
            if match := item[0].match(path):
                return item[1], match.groups(), item[2]
        return None, None


class HTTPRouting(WebsocketsRouting):
    """
    HTTPRouting is a class that is used to create a routing object for HTTP requests.

    Routing is asynchronous callable, that is it accepts scope which contains information about incoming request,
    send, an awaitable that lets you send events to the client, and receive, an awaitable which lets you receive events from the client.

    :param route: The route to the function.
    :param methods: The methods of the request.
    :param content_type: The content type of the request.
    """

    __slots__ = ("_route", "__methods", "_content_type")
    __routes: dict = {}
    __regex_routes: list = []

    def __init__(self, route, methods: list = None, content_type=None):
        if methods is None:
            methods = []
        super().__init__(route, content_type)
        self.__methods = methods or ["GET"]

    def __call__(self, fce, *args):
        if type(self._route) == Pattern:
            self.__regex_routes.append(
                (self._route, fce, self.__methods, self._content_type)
            )

        else:
            for method in self.__methods:
                if self._route not in self.__routes:
                    self.__routes[self._route] = {}
                elif method in self.__routes[self._route]:
                    raise RuntimeError(
                        f"Route alreay set! ({self.__routes.get(method, self._route)})"
                    )

                self.__routes[self._route][method] = fce, self._content_type
        return fce

    @staticmethod
    async def _options(request, response):
        path = request.path
        methods = HTTPRouting.__routes.get(
            path if path[-1] == "/" else f"{path}/", {}
        ).keys()

        if not methods:
            for item in HTTPRouting.__regex_routes:
                if item[0].match(path):
                    methods = item[2]
                    break
        if not len(methods):
            response.abort(status=404)
        response.headers.append((b"Access-Control-Allow-Headers", b"*"))
        response.headers.append(
            (b"Access-Control-Allow-Methods", ",".join(methods).encode())
        )

        response.headers.append((b"Vary", b"Access-Control-Request-Headers"))
        return b""

    @staticmethod
    def get(path: str, method: str) -> tuple:
        if method == "OPTIONS":
            return HTTPRouting._options, (), False, "text/plain"
        route = HTTPRouting.__routes.get(path if path[-1] == "/" else f"{path}/", {})
        if result := route.get(method, False):
            return result[0], (), None, result[1]
        for item in HTTPRouting.__regex_routes:
            if match := item[0].match(path):
                route = True
                if method in item[2]:
                    return item[1], match.groups(), None, item[3]
        if route and not result:
            return None, (), True, None
        return None, (), False, None
