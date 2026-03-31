import inspect
from functools import wraps

from kite.request import Request
from kite.response import Response
from kite.routenode import RouteNode


class Kite:
    def __init__(self) -> None:
        self.root = RouteNode("")

    def route(self, path: str, method: str, middleware: list):
        def decorator(func):
            sig = inspect.signature(func)

            func_args_names = list(sig.parameters.keys())
            func_args = {}

            @wraps(func)
            async def handler(req, path_params):
                if func_args_names:
                    func_args[func_args_names[0]] = req

                # func_args.update(path_params)
                for key in path_params:
                    if key in func_args_names:
                        func_args[key] = path_params[key]

                if inspect.iscoroutinefunction(func):
                    return await func(**func_args)
                return func(**func_args)

            self.root.register(
                path=path, method=method, method_handler=handler, middleware=middleware
            )

            # maybe it doesnot matter which function i return here
            # as this function is never going to be executed
            # on request the handler is going to be executed
            return func

        return decorator

    def get(self, path: str, middleware: list = []):
        return self.route(path=path, method="GET", middleware=middleware)

    def post(self, path: str, middleware: list = []):
        return self.route(path=path, method="POST", middleware=middleware)

    def put(self, path: str, middleware: list = []):
        return self.route(path=path, method="PUT", middleware=middleware)

    def delete(self, path: str, middleware: list = []):
        return self.route(path=path, method="DELETE", middleware=middleware)

    def patch(self, path: str, middleware: list = []):
        return self.route(path=path, method="PATCH", middleware=middleware)

    def options(self, path: str, middleware: list = []):
        return self.route(path=path, method="OPTIONS", middleware=middleware)

    async def read_body(self, receive):
        body = b""
        more_body = True
        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        return body

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return

        path = scope["path"]
        method = scope["method"]
        body = await self.read_body(receive)

        handler_middleware, path_params = self.root.get_handler(
            path=path, method=method
        )

        if not handler_middleware:
            response_body = Response({"message": "not found"}, status_code=404)
            await response_body.send(send)
            return

        req = Request(scope=scope, body=body, path_params=path_params)
        handler = handler_middleware["handler"]
        middleware = handler_middleware["middleware"]

        for mw in middleware:

            sig = inspect.signature(mw)
            mw_args_names = list(sig.parameters.keys())
            mw_args = {}
            if mw_args_names:
                mw_args[mw_args_names[0]] = req

            if inspect.iscoroutinefunction(mw):
                mw_response = await mw(**mw_args)
            else:
                mw_response = mw(**mw_args)

            # updating the req with whatever Request instance the
            # middleware returns
            if isinstance(mw_response, Request):
                req = mw_response
            else:
                # maybe the developer wants to stop here
                # try to return whatever the middleware returns to the client
                if not isinstance(mw_response, Response):
                    mw_response = Response(mw_response)
                await mw_response.send(send)
                return

        response_body = await handler(req, path_params)
        if not isinstance(response_body, Response):
            response_body = Response(response_body)
        await response_body.send(send)
