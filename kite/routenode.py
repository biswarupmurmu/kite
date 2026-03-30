class RouteNode:
    def __init__(self, path_segment: str) -> None:
        self.path_segment = path_segment
        # get, post, put and others will be key and the handler is value
        self.methods = {}
        # the child routes, path_segment is the key and value is RouteNode object
        self.children = {}

        self.is_param = path_segment.startswith("{") and path_segment.endswith("}")
        self.param_name = path_segment[1:-1] if self.is_param else None

    def register(self, path: str, method: str, method_handler) -> RouteNode:
        current_node = self
        segments = path.split("/")

        for segment in segments:
            if segment not in current_node.children:
                current_node.children[segment] = RouteNode(path_segment=segment)
            current_node = current_node.children[segment]
        current_node.methods[method] = method_handler
        return current_node

    def get_handler(self, path: str, method: str):
        current_node = self
        segments = path.split("/")
        extracted_params = {}

        for segment in segments:
            if segment in current_node.children:
                current_node = current_node.children[segment]
            else:
                param_node = next(
                    (
                        child
                        for child in current_node.children.values()
                        if child.is_param
                    ),
                    None,
                )
                if param_node:
                    current_node = param_node
                    extracted_params[param_node.param_name] = segment
                else:
                    return None, {}
        handler = current_node.methods.get(method, None)
        return handler, extracted_params
