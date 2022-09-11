<p align="center">
    <em>Yasgi framework a tiny, small, easy to learn, fast to code ⚡️</em>
</p>
<p align="center">
<a href="https://github.com/yezz123/yasgi/actions/workflows/test.yaml" target="_blank">
    <img src="https://github.com/yezz123/yasgi/actions/workflows/test.yaml/badge.svg" alt="Test">
</a>
<a href="https://app.codecov.io/gh/yezz123/yasgi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/yezz123/yasgi?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/yasgi" target="_blank">
    <img src="https://img.shields.io/pypi/v/yasgi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/yasgi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/yasgi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

Yasgi is a tiny, small (high-performance), web framework for building APIs with Python 3.9+ using orjson.

The key features are:

* **Tiny**: Small size and performance.
* **Fewer bugs**: Reduce about 40% of human (developer) induced errors.
* **Intuitive**: Great editor support. <abbr title="also known as auto-complete, autocompletion, IntelliSense">Completion</abbr> everywhere. Less time debugging.
* **Easy**: Designed to be easy to use, Play and Plug.
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.

## Installation

<div class="termy">

```console
$ pip install yasgi

---> 100%
```

</div>

You will also need an ASGI server, for production such as <a href="https://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> or <a href="https://github.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>.

<div class="termy">

```console
$ pip install "uvicorn[standard]"

---> 100%
```

</div>

## Example

### Create it

* Create a file `main.py` with:

```py
from yasgi import YASGI, Routing

app = YASGI(content_type="text/html")


@Routing("/endpoint", methods=["GET", "POST"])
async def endpoint(Request, Response):
     # set response header
     Response.add_header("X-header", "hello")
     # set response cookie
     Response.set_cookie("cookie_from_server", "384")
     # set response body
     return "hello world"
```

Now you should run it!

### Run it

Run the server with:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The command `uvicorn main:app` refers to:

* `main`: the file `main.py` (the Python "module").
* `app`: the object created inside of `main.py` with the line `app = YASGI()`.
* `--reload`: make the server restart after code changes. Only do this for development.

</div>

### Initializing

```py
from yasgi import YASGI

application = YASGI(content_type="application/json", allow="*", charset="UTF-8")

```

#### ASGI parameters

* `content_type` - specifies the default content type of generated responses (optional, default: `application/json`)
* `charset` - specifies the default charset generated responses (optional, default: `UTF-8`)
* `allow` - specifies global setting for `Access-Control-Allow-Origin` header - can be overwrite by passing that header to response headers (optional, default `None` - for public API should be set to `*`)

### Routing

#### Routers parameters

* `endpoint` - object should contain str or regex Pattern to match request path (mandatory)
* `type` - defines that routed is serving HTTP or WebSocket protocol (possible values: `http`, `websocket`; default: `http`)
* `methods` - list of HTTP methods to match request method - higher priority than method (optional, default: [`GET`], should be only be specified on `http` type routes)
* \*kwargs - other arguments - can be accessed by middleware in states `routed` and `end`
* `content-type`

#### Usage

Route is used as a decorator callable object you want to use as router method.
Router method takes two mandatory arguments `Request` and `Response` (explained below in a separate section).
Router method can also take variables from router regex match (if used).

#### HTTP Examples

```py
import re
from yasgi import Routing

# simple route
@Routing("/endpoint", method="GET")
# simple route method
async def routed_method_1(request, response):
     # response return without status code & mime type
     return "Response from route 1"

# re package import needed
@Routing(re.compile("/endpoint/(\d+)$"), methods=["GET", "POST"])
# regex route, with multiple methods
async def routed_method_2(request, response, number):
     # full response return
     return f"Response from route - url_number is: {number}", "200 OK", "text/html"

@Routing("/endpoint3", methods=["GET", "POST"])
#simple route, with multiple methods
async def routed_method_2(request, response):
     # alternatively can be called response method set to set response
     response.set("Response by set")

```

### Raise HTTP status

Raise HTTPStatus is used to raise HTTP status code, and optional message.

```py
from http import HTTPStatus
from yasgi import Routing

@Routing("/raise_endpoint", methods=["POST"])
async def routed_method_2(request, response):
     if not request.data:
          raise HTTPStatus("400 BAD REQUEST", "400 BAD REQUEST")
     return "data sent"
```

### Request & Response objects

Instances of these object are given to every function that is called with `@Routing` decorator.

```py
from yasgi import Routing

@Routing("/endpoint", method="GET")
async def endpoint(Request, Response):
 # instances of Request and Response objects
 pass
```

#### Request items and methods (HTTP)

* `method` - request method (GET, POST etc.) : read only
* `path` - request path: read only
* `query_params` - `dict` of query_string parameters
* `data` - request parsed data (json, -www-form-urlencoded, multipart/form-data) : read only
* `headers` - HTTP headers : read only (may contain `content_length` and `content_type` in post requests)
* `cookies` - dict contains `SimpleCookie` object of every cookie loaded
* `scope` - raw asgi scope object
* `event` - raw asgi event object

#### Response  items and methods (HTTP)

* `content_type` - response content-type : read only - can be specified in route
* `charset` - response encoding; default: `UTF-8`
* `headers` - `list` of response headers:
  * `redirect(location, status)` - redirects response to (`location`, `status` if not provide is set to `302`)
  * `set_cookie(name, value, expires=None, maxAge=None, **kwargs)` - adds cookie to response with obvious parameters, you can alow add additional arguments (`kwargs`) such as `Domain`, `Path`, `Secure`, `HttpOnly`
  * `add_header(name, value)` - adds header to response
  * `process(data, status=200)` - allow to manual process response

## Development 🚧

### Setup environment 📦

You should create a virtual environment and activate it:

```bash
python -m venv venv/
```

```bash
source venv/bin/activate
```

And then install the development dependencies:

```bash
# Install Flit
pip install flit

# Install dependencies
flit install --symlink
```

### Run tests 🌝

You can run all the tests with:

```bash
bash scripts/test.sh
```

> Note: You can also generate a coverage report with:

```bash
bash scripts/test_html.sh
```

### Format the code 🍂

Execute the following command to apply `pre-commit` formatting:

```bash
bash scripts/format.sh
```

Execute the following command to apply `mypy` type checking:

```bash
bash scripts/lint.sh
```

## License

This project is licensed under the terms of the [GNU GENERAL PUBLIC LICENSE Version 3](https://www.gnu.org/licenses/gpl-3.0.en.html).
