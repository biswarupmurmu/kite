# Welcome to Kite 🪁

Kite is a simple, lightweight, **zero-dependency** ASGI framework for Python 3.9+. It is built from the ground up to be transparent, simple, and fast. 

!!! warning "Not Production Ready"
     The purpose of this project was an attempt to understand how a web framework could be built from scratch. It is not meant to be used in any production environment as of now, as it is under active development.

But of course, if you need a tiny server without heavy bloat for a side project, give it a try. If you know what you want, it’ll get the job done—or maybe you’ll learn something even if it breaks.

## Key Features

* **Zero Dependencies:** Built entirely on the Python Standard Library.
* **O(K) Radix Tree Routing:** Instant route resolution, handling dynamic paths seamlessly.
* **Type Hints:** Built with complete type hinting so your editor's autocomplete works flawlessly out of the box.
* **ASGI Native:** Fully compatible with standard servers like Uvicorn or Hypercorn.

---

## Why

In the next few lines, I am going to tell the overly self-centered story of why I wanted to build this framework. If you don't care, you can move straight to the [Quickstart](quickstart.md) section.

You're still here to read? 🥹 Thank you, visitor. May you achieve everything you want from life.

Once upon a time.... I wanted to build a project. I never really did any project except for some full-stack(web) ones. But they don't require much effort (please don't get offended, maybe I just did the simpler ones). The rules are already defined; you follow them to create routes, controllers, middleware, and whatever other logic you need to implement, and you are done. 

As I was gradually becoming interested in how things work at a lower level, I wanted to build an HTTP server from scratch. From absolute scratch. No, I was not going to write machine code, but at least creating sockets (thanks kernel for doing the heavy tasks), getting the raw data, and then parsing that data to do whatever the HTTP server was asked to do in the request. 

As I started developing it in C, I realized it was too much work for my small brain. And AI is going to replace me anyway, so why bother creating an HTTP server from scratch? (Don't believe people if they say they built something from "scratch"). 

But doing these things and reading up gave me some understanding. And then something happened and I took a break for a few days, watched tons of movies, went on a vacation, and afterward, when I was just sitting and thinking about my life—what I've done until now, and if I'm just a below-average technical person—I decided to start a project. 

Yes, the name **Kite** sounded okay to me. I told myself, let's try to create a web framework. I once heard someone saying: *"If you are really bothered about the time complexity of your code, why did you write it in Python?"* I don't know if you needed to hear this, but I said it anyway. Hope I didn't hurt your feelings. And funny thing is Python is the only language I am kind of okay at. 

Again, I started with raw sockets. And when things got a little complex I said to myself: *"Let's be a little sane. Let's use an existing ASGI server, Uvicorn."* That way, I don't have to work with raw sockets again in my life. 

I made myself okay with developing just a framework. Uvicorn is doing the heavy lifting. Maybe this is just how software development is. We are all in debt to the cool developments that have already happened. I applied some wild ideas that I felt were cool while coding, but later I realized it doesn't matter. It doesn't matter how cool you feel while writing logic or fixing a bug—if it isn't helping the main motive, what's the point?
