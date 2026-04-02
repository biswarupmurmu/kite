# Quickstart

Let's get your first Kite server flying in under 60 seconds.

## Prerequisites

Kite takes advantage of modern Python typing and asynchronous features. You will need:

* **Python 3.9** or higher.
* An ASGI server to run the application (**Uvicorn** recommend).

!!! tip "Virtual Environments"
    It is always a good idea to create a fresh virtual environment for a new project before installing dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

## Installation

Since Kite is currently hosted on GitHub, you can install it directly via `pip`, alongside Uvicorn.

```bash
pip install git+https://github.com/biswarupmurmu/kite.git
pip install uvicorn
```

## Your First Application

Create a new file named `main.py` and add the following code:

```python
from kite import Kite, Request

# 1. Initialize the application
app = Kite()

# 2. Define a route
@app.get("/")
def read_root(req: Request):
    # 3. Return a standard Python dictionary
    return {"message": "Hello from Kite!"}
```

### What just happened?
1. **`app = Kite()`**: This creates your central ASGI application instance. This is what Uvicorn will talk to.
2. **`@app.get("/")`**: This decorator registers a `GET` request at the root URL (`/`). 
3. **`req: Request`**: Kite injects the incoming HTTP request into your function. Type-hinting it as `Request` gives your IDE full autocomplete capabilities.
4. **`return {...}`**: You don't need to manually construct JSON responses for basic data. Kite automatically detects the Python dictionary, serializes it to JSON, and attaches the correct `application/json` headers.

## Running the Server

Start the server from your terminal using Uvicorn:

```bash
uvicorn main:app --reload
```

!!! info "The `--reload` flag"
    Adding `--reload` tells Uvicorn to watch your files for changes. Whenever you save `main.py`, the server will automatically restart so you can see your updates instantly.

Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000). You should see your JSON response:

```json
{"message": "Hello from Kite!"}
```
