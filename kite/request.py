import json
from typing import Any
from urllib.parse import parse_qs


class Request:
    def __init__(self, scope, body: bytes):
        self.scope = scope
        self.method = scope.get("method", "GET")
        self.path = scope.get("path", "/")
        self.headers = self._parse_headers(scope.get("headers", []))
        self.query_params = self._parse_query_string(scope.get("query_string", b""))
        self._body = body

    def _parse_headers(self, raw_headers):
        headers = {}
        for key, value in raw_headers:
            key_str = key.decode("latin-1").lower()
            val_str = value.decode("latin-1")
            headers[key_str] = val_str
        return headers

    def _parse_query_string(self, raw_query: bytes):
        decoded_query = raw_query.decode("utf-8")
        parsed = parse_qs(decoded_query)
        return {k: v[0] for k, v in parsed.items()}

    @property
    def body(self) -> bytes:
        return self._body

    def text(self) -> str:
        return self._body.decode("utf-8")

    def json(self) -> dict[str, Any] | list[Any] | None:
        if not self._body:
            return None
        try:
            return json.loads(self.text())

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body provided.")

    def json_dict(self) -> dict[str, Any]:
        data = self.json()
        if not isinstance(data, dict):
            raise ValueError("Expected a json(dictionary)")
        return data

    def json_list(self) -> list[Any]:
        data = self.json()
        if not isinstance(data, list):
            raise ValueError("Expected a json(list)")
        return data
