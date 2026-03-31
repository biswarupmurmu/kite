import asyncio
import mimetypes
import os


class FileResponse:
    def __init__(
        self, path: str, filename: str | None = None, chunk_size=65536
    ) -> None:
        self.path = path
        self.filename = filename or os.path.basename(path)
        self.chunk_size = chunk_size

    async def send(self, send_func) -> None:
        if not os.path.exists(self.path):
            await self._send_404(send_func)
            return

        mime_type, _ = mimetypes.guess_type(self.path)
        content_type = mime_type or "application/octet-stream"

        file_size = os.path.getsize(self.path)

        headers = [
            (b"content-type", content_type.encode("utf-8")),
            (b"content-length", str(file_size).encode("utf-8")),
            (
                b"content-disposition",
                f"attachment; filename='{self.filename}'".encode("utf-8"),
            ),
        ]
        await send_func(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": headers,
            }
        )

        with open(self.path, "rb") as f:
            while True:
                chunk = await asyncio.to_thread(f.read, self.chunk_size)

                if not chunk:
                    await send_func(
                        {"type": "http.response.body", "body": b"", "more_body": False}
                    )
                    break

                await send_func(
                    {"type": "http.response.body", "body": chunk, "more_body": True}
                )

    async def _send_404(self, send_func) -> None:
        await send_func(
            {
                "type": "http.response.start",
                "status": 404,
                "headers": [(b"content-type", b"application/json")],
            }
        )

        await send_func(
            {
                "type": "http.response.body",
                "body": b"{'message': 'file not found'}",
                "more_body": False,
            }
        )
