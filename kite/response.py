import json
from typing import Any


class Response:
    def __init__(
        self,
        body: Any = "",
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.raw_headers = headers or {}
        self.body_bytes = self.prepare_body(body)

    def prepare_body(self, body: Any):
        if isinstance(body, (dict, list)):
            self.raw_headers["content-type"] = "application/json"
            return json.dumps(body).encode("utf-8")

        if isinstance(body, str):
            self.raw_headers["content-type"] = "text/plain; charset=utf-8"
            return body.encode("utf-8")

        if isinstance(body, bytes):
            self.raw_headers["content-type"] = "application/octet-stream"
            return body

        self.raw_headers["content-type"] = "text/plain; charset=utf-8"
        return str(body).encode("utf-8")

    @property
    def asgi_headers(self) -> list[tuple[bytes, bytes]]:
        return [
            (key.lower().encode("latin-1"), value.lower().encode("latin-1"))
            for key, value in self.raw_headers.items()
        ]

    async def send(self, send_func):
        await send_func(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.asgi_headers,
            }
        )

        await send_func(
            {
                "type": "http.response.body",
                "body": self.body_bytes,
            }
        )
