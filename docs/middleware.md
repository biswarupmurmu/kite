# Middleware Pipeline

Middleware allows you to intercept and process requests before they ever reach your core route handlers. 

Kite implements middleware as a straightforward **Sequential Pipeline**. You can visualize it as a list of functions where the `Request` object is passed from one function to the next, much like an assembly line.

## Registering Middleware

You attach middleware to a route by passing a list of functions to the `middleware` parameter of the routing decorator. They are executed in the exact sequence they appear in the list.

```python
@app.get("/dashboard", middleware=[verify_token, attach_user_data])
def dashboard_handler(req: Request):
    return {"user": req.user_id}
```

Just like route handlers, Kite supports both asynchronous (`async def`) and standard (`def`) middleware functions in the same list. 

!!! warning "Don't block the loop"
    Never execute heavy, blocking synchronous code (like `time.sleep()` or a massive while-loop) inside an `async def` middleware function. Because it runs on the main event loop, a blocking operation will freeze the entire server and force all other requests to wait.


## The Two Rules of Middleware

Because Kite iterates through your middleware list sequentially, every middleware function has a choice to make: **continue the chain** or **halt execution**.

### 1. Continuing the Chain
If your middleware successfully does its job (like logging, or modifying headers), it **must return the `Request` object**. Kite will take this returned object and pass it to the next middleware in the list, or finally to the route handler.

You can freely attach new data directly to the `req` object to pass state down the line.

```python
async def attach_user_data(req: Request):
    # You can access path parameters directly from the request here
    tenant_id = req.path_params.get("tenant_id")
    
    # Fetch data and attach it to the request object
    req.user_role = await db.get_role(tenant_id)
    
    # MUST return the request to continue the pipeline
    return req 
```

### 2. Halting Execution (Short-Circuiting)
If your middleware decides that the request should be rejected (e.g., a missing authentication token, or a rate limit exceeded), you can immediately halt the pipeline.

To stop execution, simply return a standard response type (a `dict`, `str`, or a Kite `Response` object). Kite will instantly stop processing the middleware list, ignore the main route handler, and send your response directly back to the client.

```python
from kite import Request, Response

def require_auth(req: Request):
    token = req.headers.get("authorization")
    
    if not token:
        # Returning a dictionary automatically creates a 200 OK Response,
        # but to properly reject auth, we return an explicit 401 Response.
        # This halts the pipeline immediately.
        return Response(
            status_code=401, 
            body={"error": "Missing authorization token"}
        )
        
    # Validation passed, continue the chain
    return req
```

## A Complete Pipeline Example

Here is how a fully assembled pipeline looks, demonstrating both continuation and halting.

```python
from kite import Kite, Request, Response

app = Kite()

# 1. First middleware checks for the token
def auth_guard(req: Request):
    if req.headers.get("x-api-key") != "supersecret":
        return {"error": "unauthorized"} # Halts execution!
    return req # Continues

# 2. Second middleware modifies the request
def add_timestamp(req: Request):
    req.start_time = "12:00:00"
    return req # Continues

# 3. The Handler
@app.get("/data", middleware=[auth_guard, add_timestamp])
def get_data(req: Request):
    # This is only executed if the auth_guard passed
    return {
        "status": "success", 
        "process_started_at": req.start_time
    }
```
