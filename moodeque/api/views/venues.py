
from moodeque.api.views import (BaseView,
                                MatchBaseView)
from pyramid.view import (view_defaults,
                          view_config)
from moodeque.models import (Venue,
                             User)
from collections import Counter
from pyramid.httpexceptions import HTTPNotFound
from random import randrange

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
        for u in users:
            moods[u.mood] += 1

        song = None if not len(self.venue.playlist) else \
                self.venue.playlist[-1].to_dict()

        return dict(
            venue=venue,
            people_count=len(list(self.venue.people)),
            current_song=song,
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
        songs = []
        try:
            self.log.info("Playlist: {}".format(len(self.venue.playlist)))
            if len(self.venue.playlist) == 1:
                songs = [self.venue.playlist[0].to_dict()]
            else:
                songs = [s.to_dict() for s in self.venue.playlist]
            return {"playlist": songs}

        except Exception as e:
            self.log.exception(str(e))
            raise e


@view_defaults(route_name="song")
class SongView(VenueBase):
    methods = ('next', 'current', 'previous')

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        if self.method not in self.methods:
            raise HTTPNotFound()
        return getattr(self, self.method)()

    def current(self):
        return self.venue.playlist[-1].to_dict()

    def next(self):
        limit = int(self.request.params.get('limit', 1))
        mood = self.venue.overall_mood
        songs = self.request.stereomood.search_by_mood(mood, limit=20)
        songs = [songs[randrange(0, 19, 1)]]
        result = []
        for s in songs:
            new_s = self.request.stereomood.download_song(s, 
                        self.request.registry.settings['moodeque.song_cache_path'])
            song_d = new_s.to_dict()
            song_d['audio_url'] = "{0}/{1}.mp3".format(
                self.request.registry.settings["moodeque.song_url"],
                new_s.id
            )
            result.append(song_d)
            self.venue.play(new_s)
        return {
            "songs": result
        }

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


@view_defaults(route_name="customer")
class CustomerView(VenueBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return User.find(self.request.db, self.uid).to_dict()

    def post(self):
        self.log.info("User {} checked in into {}", self.uid, self.venue)
        user = User.find_by_name(self.request.db, self.uid)
        user.checkin(self.venue)
        return user.to_dict()

    def delete(self):
        self.log.info("User {} checked out from {}", self.uid, self.venue)
        user = User.find_by_name(self.request.db, self.uid)
        user.checkout(self.venue)
        return user.to_dict()
