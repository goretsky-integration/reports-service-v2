import httpx


__all__ = ("ConnectionResponseParseError",)


class ConnectionResponseParseError(Exception):
    def __init__(self, *args, response: httpx.Response) -> None:
        super().__init__(*args)
        self.response = response
