
from moodeque.api.views import (BaseView,
                                MatchBaseView)
from pyramid.view import (view_defaults,
                          view_config)


@view_defaults(route_name="venues")
class VenuesView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def post(self):
        return {}


@view_defaults(route_name="venue")
class VenueView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        self.log.info("Getting info on venue {0}".format(self.venueid))
        return {}

    def post(self):
        return {}

    def delete(self):
        return {}


@view_defaults(route_name="playlist")
class PlaylistView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}


@view_defaults(route_name="song")
class SongView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}


@view_defaults(route_name="customers")
class CustomersView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def post(self):
        return {}

    def delete(self):
        return {}


@view_defaults(route_name="customer")
class CustomerView(MatchBaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return {}

    def delete(self):
        return {}
