
from pyramid.httpexceptions import HTTPMethodNotAllowed
import logging


class BaseView(object):

    def __init__(self, request):
        self.request = request
        self.log = logging.getLogger("{0}:{1}".format(__name__,
                                                      self.__class__.__name__))

    def _dispatch(self, *args, **kwargs):
        try:
            method = getattr(self, self.request.method.lower())
        except AttributeError:
            raise HTTPMethodNotAllowed()

        return method(*args, **kwargs)

    def head(self):
        result = self.get()
        response.body = ''
        response.headers.update(
            {'Content-Length': 0,
             'Content-Type': 'application/json; charset=UTF-8'}
        )
        return response


class MatchBaseView(BaseView):

    def __init__(self, request):
        super(MatchBaseView, self).__init__(request)
        for k, v in self.request.matchdict.iteritems():
            setattr(self, k, v)
