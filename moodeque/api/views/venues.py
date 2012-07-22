
from moodeque.api.views import (BaseView,
                                MatchBaseView)
from pyramid.view import (view_defaults,
                          view_config)
from moodeque.models import (Venue,
                             User)
from collections import Counter

class VenueBase(MatchBaseView):

    def __init__(self, request):
        super(VenueBase, self).__init__(request)
        self.venue = Venue.find(self.request.db, self.venueid)


@view_defaults(route_name="venues")
class VenuesView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):

        venues = [ v.to_dict() for v in Venue.all(self.request.db)]
        return {
            "venues": venues
        }

    def post(self):
        venue = Venue.create(self.request.db,
            name = request.params['name'],
            description = request.params['description'],
            latitude = request.params['latitude'],
            longitude = request.params['longitude']
        )
        request.response.code = 201
        return venue.to_dict()


@view_defaults(route_name="venue")
class VenueView(VenueBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        venue = self.venue.to_dict()
        users = self.venue.people
        moods = Counter()
        for u in user:
            moods[u.mood] += 1

        return dict(
            venue=venue,
            people_count=len(self.venue.people),
            current_song=self.playlist[-1].to_dict(),
            moods=moods
        )

    def put(self):
        modified = False
        for attr in ("name", "description", "latitude", "longitude"):
            if attr in self.request.params:
                setattr(self.venue, attr, self.request.params[attr])
                modified = True

        if modified:
            self.venue.save()
        return self.venue.to_dict()

    def delete(self):
        self.venue.destroy()
        return self.venue.to_dict()


@view_defaults(route_name="playlist")
class PlaylistView(VenueBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        songs = [s.to_dict() for s in self.venue.playlist]
        return {"playlist": songs}


@view_defaults(route_name="song")
class SongView(VenueBase):
    methods = ('next', 'current', 'previous')

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        if self.method not in self.methods:
            raise HTTPNotFound()
        return getattr(self, method)()

    def current(self):
        return self.venue.playlist[-1].to_dict()

    def next(self):
        limit = self.request.params.get('limit', '1')
        mood = self.venue.overall_mood
        songs = self.request.stereomood.search_by_mood(mood, limit=limit)
        return [s.to_dict() for s in songs]

    def previous(self):
        index = int(self.request.params.get('index', 1))
        return self.venue.playlist[-index].to_dict()


@view_defaults(route_name="customers")
class CustomersView(VenueBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return [u.to_dict() for u in self.venue.users]

    def post(self):
        user = User.find(self.request.db, self.request.params['user'])
        user.checkin(self.venue)
        return user.to_dict()


@view_defaults(route_name="customer")
class CustomerView(VenueBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return User.find(self.request.db, self.uid).to_dict()

    def delete(self):
        user = User.find(self.request.db, self.uid)
        user.checkout(self.venue)
        return user.to_dict()
