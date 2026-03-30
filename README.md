# Kite Framework 🪁

A lightning-fast, zero-dependency ASGI web framework for Python. 

## 📖 The Story (Why I Built This)

I built Kite because I wanted to look under the hood. We use massive, powerful frameworks every day, but I wanted to understand how they actually work from scratch.

**To be completely honest:** Kite is a hobby project. It is not going to replace FastAPI, Flask, or Django in a production environment anytime soon, and it wasn't built to. 

It was built out of pure curiosity. But, if you want to see how a web framework is built from the ground up, need a tiny, transparent router for a side project, or just want to tinker with zero dependencies—give it a try! You can read the entire source code in one sitting.

---

## ✨ What's Inside?

* **Zero Dependencies:** Built entirely on the Python Standard Library. No pip installing 3rd party packages.
* **O(K) Radix Tree Routing:** Instant route resolution for maximum performance, seamlessly handling dynamic path parameters (e.g., `/users/{id}`).
* **Type-Safe Everywhere:** I tried to be as type-safe as possible throughout the entire codebase. Every function return and built-in method (like `req.json_dict()`) is strictly typed to keep your IDE's LSP perfectly happy.
* **ASGI Native:** Fully compatible with standard servers like Uvicorn.

---

## 🚀 Installation

Because Kite relies on zero external packages, it is incredibly portable. 

**Option 1: The Drop-In Method (Easiest)**
Simply download the `kite/` folder and place it directly into your project directory next to your application code.

**Option 2: Install via pip from GitHub**

```bash
pip install git+https://github.com/biswarupmurmu/kite.git
```

---

## 💻 Quick Start

Create a file named `main.py` and write your first API:

```python
from kite import Kite, Request, Response

app = Kite()

# A simple GET route
@app.get("/")
def home(req: Request):
    # Kite automatically wraps dicts in a JSON Response!
    return {"message": "Welcome to Kite!"}

# Dynamic Path Parameters & JSON Parsing
@app.post("/users/{user_id}")
async def create_user(req: Request, user_id: str):
    data = req.json_dict()
    
    return Response(
        status_code=201,
        body={
            "id": user_id,
            "name": data.get("name"),
            "status": "created"
        }
    )
```

### Running the Server

To run your backend API you will need to install an ASGI server of your choice. 

You can use standard servers like **Uvicorn**, **Hypercorn**, or **Daphne**. 

```bash
# Install your preferred ASGI server
pip install uvicorn

# Run your Kite app
uvicorn main:app --reload
```

---

## 🗺️ Roadmap (What's Next)

Since this is an evolving learning project, here is the roadmap of features I am currently building or planning to tackle next:

* [x] **Query Parameters:** Automatically extract URL queries (e.g., `?limit=10`) into a usable Python dictionary.
* [ ] **Middleware System:** Support for Global (Onion-model) middleware and Route-specific middleware pipelines for things like authentication and CORS.
* [ ] **Dependency Injection:** A clean way to pass database connections into route handlers safely.
* [ ] **Automated Testing:** Building out a comprehensive test suite using Python's built-in `unittest`.

*(If you have any suggestions, ideas, or feedback on what I should build next, they are incredibly welcome!)*

---

## 🤝 Contributing & Learning

If you are also curious about how frameworks work, I'd love for you to poke around the code! Feel free to open an issue, submit a pull request, or just use parts of this code to build your own tools.

## 📄 License
MIT License.
