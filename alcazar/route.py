import inspect
from http import HTTPStatus

from parse import parse

from alcazar.constants import ALL_HTTP_METHODS
from alcazar.exceptions import HTTPError


class Route:
    def __init__(self, path_pattern, handler, methods=None):
        if methods is None:
            methods = ALL_HTTP_METHODS

        self._path_pattern = path_pattern
        self._handler = handler
        self._methods = [method.upper() for method in methods]

    def match(self, request_path):
        result = parse(self._path_pattern, request_path)
        return (True, result.named) if result is not None else (False, None)

    def handle_request(self, request, response, **kwargs):
        if inspect.isclass(self._handler):
            handler = getattr(self._handler(), request.method.lower(), None)
            if handler is None:
                raise HTTPError(status=HTTPStatus.METHOD_NOT_ALLOWED)
        elif request.method in self._methods:
            handler = self._handler

        else:
            raise HTTPError(status=HTTPStatus.METHOD_NOT_ALLOWED)

        handler(request, response, **kwargs)
