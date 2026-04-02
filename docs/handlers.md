# Request Handlers

In Kite, a request handler is simply a Python function that takes an incoming `Request` object and returns data back to the client. 

Because Kite is built directly on the ASGI specification, its core is fundamentally asynchronous. However, it does not force you to write asynchronous code if your specific route doesn't need it. Kite intelligently inspects your route handlers at startup and routes them to the correct execution context automatically.

You can seamlessly mix standard `def` functions and `async def` functions within the exact same application.

## Async vs. Sync Execution

Here is how you define both types of handlers:

```python
import asyncio
from kite import Request

# Asynchronous handler: Runs directly on the main ASGI event loop
@app.get("/async")
async def async_task(req: Request):
    # The 'await' yields control back to the server while waiting
    await asyncio.sleep(1) 
    return {"type": "asynchronous"}

# Synchronous handler: Runs in an isolated background thread
@app.get("/sync")
def sync_task(req: Request):
    # Kite automatically offloads this so it doesn't block other users
    return {"type": "synchronous"}
```

### When to use `async def`
Use asynchronous handlers when your endpoint is **I/O-bound**—meaning it spends most of its time waiting for external systems. When your function hits an `await` keyword, it yields control back to Kite's event loop. This allows the server to handle other incoming requests while your function waits in the background.

**Best for:**

* Querying databases (e.g., PostgreSQL, Redis)
* Making external HTTP requests to other APIs
* Reading or writing files to disk

!!! warning "Don't block the loop"
    Never execute heavy, blocking synchronous code (like `time.sleep()` or a massive while-loop) inside an `async def` function. Because it runs on the main event loop, a blocking operation will freeze the entire server and force all other requests to wait.

### When to use standard `def`
Use standard synchronous handlers when your endpoint is **CPU-bound** or when you are just returning simple, static data. 

When you define a handler with a standard `def`, Kite knows it might contain blocking code. To protect the main server, Kite automatically offloads the execution of that function to a separate background thread. This ensures that even if your synchronous function takes 5 seconds to do something, the main asynchronous event loop remains completely unblocked and fast.

**Best for:**

* Heavy mathematical computations or data processing
* Simple endpoints that just return a basic dictionary
* Integrating with older, non-async third-party libraries

!!! tip "The Rule of Thumb"
    If you are calling a library that requires `await` (like `httpx`), use `async def`. If you are using standard blocking libraries (like `requests` or `sqlalchemy`), use standard `def`.
