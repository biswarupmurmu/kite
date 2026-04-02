# Routing & Parameters

Kite uses a custom Radix Tree routing engine. This means your routes are resolved in O(K) time, making it incredibly fast even as your application grows.

## Basic Routing
Use the HTTP method decorators on your `Kite` app instance to register static endpoints:

```python
@app.get("/ping")
def ping(req: Request):
    return {"status": "ok"}

@app.post("/submit")
def submit_data(req: Request):
    return {"status": "created"}
```

## Path Parameters
You can capture dynamic values directly from the URL by wrapping the segment in `{}`. 

Kite gives you two seamless ways to access these extracted values:

**1. As Keyword Arguments (Recommended)**
The extracted value is automatically injected as a keyword argument into your route handler. 

**2. The `path_params` Dictionary**
All captured parameters are simultaneously stored in the `req.path_params` dictionary, giving you raw access to the routing state.

```python
@app.get("/users/{user_id}")
def get_user(req: Request, user_id: str):
    # Method 1: Using the injected keyword argument
    print(f"Injected ID: {user_id}")
    
    # Method 2: Reading directly from the Request object
    dict_id = req.path_params.get("user_id")
    
    return {
        "requested_id": user_id, 
        "dict_id": dict_id
    }
```
!!! info "Data Types"
    Remember that path parameters are fundamentally strings. If you need an integer or any other data type, you will need to cast it manually inside your handler.

!!! tip "Type Hinting"
    Always type-hint your path parameters in the handler function signature (e.g., `user_id: str`). It keeps your IDE's LSP perfectly happy and makes your codebase self-documenting.

## Query Parameters
Query parameters (e.g., `?limit=10&sort=desc`) are automatically parsed by the framework and attached to the `Request` object.

```python
@app.get("/search")
def search(req: Request):
    # Extracts ?query=python from the URL, defaulting to "default" if missing
    search_term = req.query_params.get("query", "default")
    limit = req.query_params.get("limit", "10")
    
    return {
        "results_for": search_term,
        "limit": int(limit)
    }
```

!!! info "Data Types"
    Remember that raw HTTP query parameters are fundamentally strings. If you need an integer (like the `limit` example above) or a boolean, you will need to cast it manually inside your handler.

