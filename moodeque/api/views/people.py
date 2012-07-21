from moodeque.api.views import (BaseView,
                                MatchBaseView)
from pyramid.view import (view_defaults,
                          view_config)


@view_defaults(route_name="people")
class PeopleView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def post(self):
        return {}


@view_defaults(route_name="person")
class PersonView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def put(self):
        return {}

    def delete(self):
        return {}


@view_defaults(route_name="login")
class LoginView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def post(self):
        return {}


@view_defaults(route_name="mood")
class MoodView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def put(self):
        return {}
