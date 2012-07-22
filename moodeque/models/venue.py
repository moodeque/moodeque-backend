from collections import Counter

from moodeque.models import rediscoll
from moodeque.models import playlist


class Venue(object):
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

    @classmethod
    def dbname(cls, venueid):
        return "venue.%s" %(str(venueid))

    @classmethod
    def dbindex(cls):
        return "venues"

    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" %(PlayList.dbindex()))

    @classmethod
    def create(cls, db, description, latitude, longitude):
        venueid = Venue.autoid()
        robj = Venue(db, venueid, description, latitude, longitude)
        idx = rediscoll.Set(Venue.dbindex(), db)
        idx.add(Venue.dbname(venueid))
        robj.save()
        return robj

    @classmethod
    def find(cls, db, venueid):
        robj = rediscoll.Hash(Venue.dbname(venueid), db)
        venue = Venue(db, venueid,
                      robj['description'],
                      robj['latitude'],
                      robj['longitude'])
        venue._last_mood = robj['last_mood']
        venue._playlist = playlist.PlayList.find(db, venueid)

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(Venue.dbindex(), db)
        return robj.all()

    def save(self):
        robj = rediscoll.Hash(Venue.dbname(self.venueid), self._db)
        robj['description'] = self.description
        robj['latitude'] = self.latitude
        robj['longitude'] = self.longitude

    def destroy(self):
        idx = rediscoll.Set(Venue.dbindex(), self._db)
        idx.remove(self.venueid)
        self._db.delete(Venue.dbname(self.venueid))

    def __init__(self, db, venueid, description, latitude, longitude):
        self.venueid = venueid
        self.description = description
        self.latituide = latitude
        self.longitude = longitude
        self._db = db
        self._last_mood = None
        self._playlist = playlist.PlayList(name, db)
        self._user_moods = crowd.Crowd(name, db)
        self._user_group = population.Population(name, db)

    def overall_mood(self):
        """
        Returns the overall combined mood of all the users in the venue.
        The greater the value, the stronger the feeling.
        """
        counter = Counter(self.MOODS)

        for user in self.users():
            user_mood = self.MOODS[user.mood]
            counter[user_mood] += 1

        return counter.most_common(1)[0]

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

    def play(self, song):
        """
        Registers the given song as the one currently being played.
        """
        raise NotImplementedError

    def get_in_playlist(self, index):
        "index sempre negativo, ritorna oggetto song"
        raise NotImplementedError

    def users(self):
        """
        Returns an iterable containing of all the users objects currently in the venue.
        """
        raise NotImplementedError

