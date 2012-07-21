import logging
from pyramid.view import view_config
from pyramid.httpexceptions import (HTTPBadRequest, 
                                    HTTPNotFound)


log = logging.getLogger(__name__)


def generate_empty_response(context, request, status, add_headers={}):
    response = request.response
    response.status_int = status
    if hasattr(context, 'headers') and context.headers:
        response.headers = context.headers
    response.headers.update(
        {'Content-Length': 0,
         'Content-Type': 'application/json; charset=UTF-8'}
    )
    response.body = ''
    response.headers.update(add_headers)
    # TODO add logging with ip/user/agent etc etc
    log.info("Generating empty response [status: %s, headers:%s]",
              status, response.headers)
    log.debug("request: %s", request)
    log.debug("response: %s", response)
    return response


@view_config(context=HTTPBadRequest)
@view_config(context=HTTPNotFound)
def created(context, request):
    return generate_empty_response(context, request, context.code)


@view_config(context=KeyError)
def invalid_params(context, request):
    return generate_empty_response(context, request, 400)


@view_config(context=NotImplementedError)
def not_implemented(context, request):
    return generate_empty_response(context, request, 501)