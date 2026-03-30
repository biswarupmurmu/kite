import inspect
from functools import wraps

from kite.request import Request
from kite.response import Response
from kite.routenode import RouteNode


class Kite:
    def __init__(self) -> None:
        self.root = RouteNode("")

    def route(self, path, method):
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

            self.root.register(path=path, method=method, method_handler=handler)

            # maybe it doesnot matter which function i return here
            # as this function is never going to be executed
            # on request the handler is going to be executed
            return func

        return decorator

    def get(self, path):
        return self.route(path=path, method="GET")

    def post(self, path):
        return self.route(path=path, method="POST")

    def put(self, path):
        return self.route(path=path, method="PUT")

    def delete(self, path):
        return self.route(path=path, method="DELETE")

    def patch(self, path):
        return self.route(path=path, method="PATCH")

    def options(self, path):
        return self.route(path=path, method="OPTIONS")

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

        handler, params = self.root.get_handler(path=path, method=method)

        req = Request(scope, body)

        if handler:
            response_body = await handler(req, params)
            if not isinstance(response_body, Response):
                response_body = Response(response_body)
        else:
            response_body = Response({"message": "not found"}, status_code=404)

        await response_body.send(send)
