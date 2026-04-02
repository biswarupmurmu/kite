# Requests & Responses

Kite provides a clean, intuitive interface to interact with incoming HTTP data and format outbound responses. It abstracts away the complex ASGI byte streams into easy-to-use Python classes.

## The `Request` Object

Every route handler receives a `Request` object. This object automatically parses the raw ASGI scope and provides immediate access to the routing state, headers, and body.

### Properties
You have direct access to the following pre-parsed properties:

* `req.method` - The HTTP method (e.g., `"GET"`, `"POST"`).
* `req.path` - The requested URL path.
* `req.headers` - A dictionary of request headers. Kite automatically decodes these and converts all keys to lowercase for easy lookup.
* `req.query_params` - A dictionary of parsed query string parameters.
* `req.path_params` - A dictionary of dynamic path segments captured by the router.

### Reading the Body
Kite provides several strictly-typed methods to safely read the incoming request body, depending on the format you expect.

```python
@app.post("/upload")
async def handle_upload(req: Request):
    # 1. Raw bytes
    raw_data: bytes = req.body
    
    # 2. Decoded string
    text_data: str = req.text()
    
    # 3. Dynamic JSON (Returns dict or list depending on payload)
    json_data = req.json()
```

!!! tip "Strictly Typed JSON Methods"
    If you know exactly what kind of JSON payload your endpoint should receive, use Kite's strict JSON methods: `req.json_dict()` or `req.json_list()`. 
    
    These methods keep your IDE's LSP perfectly happy and will actively raise a `ValueError` if the client sends a list when you expected a dictionary.

```python
@app.post("/items")
async def create_item(req: Request):
    # Guarantees a dictionary and provides perfect autocomplete!
    data: dict = req.json_dict() 
    
    return {"saved": data.get("name")}
```

## Responses

When returning data from a handler, you have two options: rely on Kite's automatic response wrapping, or explicitly construct a `Response` object.

### Automatic Responses
By default, if you return a native Python type, Kite automatically wraps it in a `200 OK` Response and sets the correct `Content-Type` header for you.

```python
@app.get("/auto")
def auto_response(req: Request):
    # Automatically returns with Content-Type: application/json
    return {"status": "success", "data": [1, 2, 3]}

@app.get("/text")
def auto_text(req: Request):
    # Automatically returns with Content-Type: text/plain
    return "Hello, World!"
```

### Explicit Responses
If you need to change the HTTP status code, attach custom headers, or bypass the automatic content detection, return a `Response` object explicitly.

```python
from kite import Response

@app.post("/auth")
def login(req: Request):
    # Returning a 401 Unauthorized with custom headers
    return Response(
        status_code=401,
        body={"error": "Invalid credentials"},
        headers={"X-Auth-Attempt": "Failed"}
    )
```

!!! info "Content-Type Inference"
    When you pass data to a `Response` object, Kite infers the `Content-Type` based on the Python type:

    * `dict` or `list` → `application/json`
    * `str` → `text/plain; charset=utf-8`
    * `bytes` → `application/octet-stream`
    * Anything else is cast to a string and served as `text/plain`.

## File Downloads & Streaming

To handle file downloads safely and efficiently, Kite provides a dedicated `FileResponse` class.

Instead of reading the whole file at once, `FileResponse` asynchronously streams the file from your disk to the client in small chunks (default 64KB). It uses background threads for the disk I/O (`asyncio.to_thread`), ensuring your main ASGI event loop is never blocked during the transfer.

```python
from kite import FileResponse, Request

@app.get("/download/report")
async def download_file(req: Request):
    # Kite handles the chunking, MIME-type guessing, and headers automatically
    return FileResponse(
        path="./assets/annual_report.pdf",
        filename="custom_report_name.pdf" # Optional: overrides the downloaded file name
    )
```

### Under the Hood Features

When you return a `FileResponse`, Kite automatically handles these:

* **MIME Type Inference:** It automatically detects the correct `Content-Type` (e.g., `application/pdf` or `image/jpeg`) based on the file extension.
* **Smart Headers:** It automatically calculates and attaches the `Content-Length` header so the user's browser displays an accurate download progress bar.
* **Forced Download:** It automatically sets the `Content-Disposition: attachment` header, which prompts the user's browser to download and save the file rather than trying to open it directly in the tab.
* **Built-in 404s:** If the requested file path does not exist, `FileResponse` safely catches it and returns a standard `404 Not Found` JSON response instead of crashing the server.

!!! tip "Customizing Chunk Size"
    If you are streaming massive files (like gigabytes of video data) and want to reduce the number of disk reads, you can easily increase the buffer size: `FileResponse(path="...", chunk_size=1024 * 1024) # 1MB chunks`
