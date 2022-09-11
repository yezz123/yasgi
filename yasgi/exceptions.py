class InputParseError(Exception):
    """Exception raised when the input is not valid"""

    def __init__(
        self,
        e: Exception,
        message: str = "Input parse error",
    ):
        super().__init__(message)
        self.e = e


class HTTPAbort(Exception):
    """Exception raised when the request should be aborted."""

    def __init__(self, message: str = "HTTP abort", status: int = 500):
        super().__init__(message)
        self.status = status
