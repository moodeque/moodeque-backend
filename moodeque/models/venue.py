# part of moodeque

from . import rediscoll
from moodeque.models import playlist
from moodeque.models.base import (BaseModel,
                                  RedisModel)


class Venue(BaseModel, RedisModel):
    """
    This class represents a Moodeque venue.
    A Venue is any place where music is played, users gather and they (hopefully)
    have fun and interact.
    """
    export_attrs = ('description', 'latitude', 'longitude')

    db_attrs = ('description', 'latitude', 'longitude')

    @classmethod
    def dbname(cls, venueid):
        return "venue.%s" %(str(venueid))

    def destroy(self):
        self._playlist.destroy()
        idx = rediscoll.Set(cls.dbindex(), self._db)
        idx.remove(self.venueid)
        self._db.delete(cls.dbname(self.venueid))

    def __init__(self, db, venueid, description, latitude, longitude):
        super(Venue, self).__init__(db, venueid)
        self.venueid = venueid
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self._db = db
        self._playlist = playlist.PlayList(name, db)

    def overall_mood(self):
        """
        Returns the overall combined mood of all the users in the venue.
        A positive value indicates a good mood.
        A negative value indicates a bad mood.
        The greater the value, the stronger the feeling.
        """
        raise NotImplementedError

    def checkin(self, user):
        """
        Register an user in the venue. The user will now contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError

    def checkout(self, user):
        """
        Deregister an user from the venue. The user will no longer contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError

    @property
    def playlist(self):
        """
        Returns l'oggetto playlist.
        The currently played song is always the first one, the others
        following in reverse played order.
        """
        raise NotImplementedError

    @property
    def people(self):
        """
        Returns an iterable containing of all the users objects currently in the venue.
        """
        raise NotImplementedError

    def play(self, song):
        """
        Registers the given song as the one currently being played.
        """
        raise NotImplementedError

    def get_in_playlist(self, index):
        "index sempre negativo, ritorna oggetto song"
        raise NotImplementedError


