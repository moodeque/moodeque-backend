# part of moodeque

from . import rediscoll
from moodeque.models import crowd
from moodeque.models import playlist
from moodeque.models.user import User
from moodeque.models.base import (BaseModel,
                                  RedisModel)


class Venue(BaseModel, RedisModel):
    """
    This class represents a Moodeque venue.
    A Venue is any place where music is played, users gather and they (hopefully)
    have fun and interact.
    """

    MOODS = (
        'crap',
        'sad',
        'melancholy',
        'worried',
        'serious',
        'cool',
        'optimistic'
        'energetic',
        'happy',
        'mad',
    )

    export_attrs = ('name', 'description', 'latitude', 'longitude')

    db_attrs = ('name', 'description', 'latitude', 'longitude', 'crowd_id', 'playlist_id')

    @classmethod
    def dbname(cls, venueid):
        return "venue.%s" %(str(venueid))

    @classmethod
    def dbindex(cls):
        return "venues"

    @classmethod
    def setup(cls, obj, db):
        obj._playlist = playlist.Playlist.create(db)
        obj._crowd = crowd.Crowd.create(db)
        obj.playlist_id = obj._playlist.plid
        obj.crowd_id = obj._crowd.crid

    @classmethod
    def shutdown(cls, obj, db):
        obj._playlist.destroy()
        obj._crowd.destroy()

    @classmethod
    def lookup(cls, obj, db):
        obj._playlist = playlist.Playlist.find(db, obj.playlist_id)
        obj._crowd = crowd.Crowd.find(db, obj.crowd_id)
        obj.playlist_id = obj._playlist.plid
        obj.crowd_id = obj._crowd.crid

    def __init__(self, db, venueid, **kwargs):
        super(Venue, self).__init__(db, venueid, **kwargs)

    def overall_mood(self):
        """
        Returns the overall combined mood of all the users in the venue.
        The greater the value, the stronger the feeling.
        """
        counter = Counter(self.MOODS)

        for user in self.people():
            user_mood = self.MOODS[user.mood]
            counter[user_mood] += 1

        return counter.most_common(1)[0]

    def checkin(self, user):
        """
        Register an user in the venue. The user will now contribute to
        the overall mood of the venue.
        """
        self._crowd.add(user.userid)

    def checkout(self, user):
        """
        Deregister an user from the venue. The user will no longer contribute to
        the overall mood of the venue.
        """
        self._crowd.remove(user.userid)

    @property
    def playlist(self):
        """
        Returns l'oggetto playlist.
        The currently played song is always the first one, the others
        following in reverse played order.
        """
        return self._playlist

    @property
    def people(self):
        """
        Returns an iterable containing of all the users objects currently in the venue.
        """
        return (User.find(self._db, uid) for uid in self._crowd.all())

    def play(self, song):
        """
        Registers the given song as the one currently being played.
        """
        self._playlist.append(song)

    def get_in_playlist(self, index):
        "index sempre negativo, ritorna oggetto song"
        return self._playlist[index]
