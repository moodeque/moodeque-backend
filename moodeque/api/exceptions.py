import logging
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
