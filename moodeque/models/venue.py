# (C) 2012 Francesco Romani <fromani . gmail . com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


from moodeque.models import rediscoll
from moodeque.models import playlist


class Venue(object):
    """
    This class represents a Moodeque venue.
    A Venue is any place where music is played, users gather and they (hopefully)
    have fun and interact.
    """
    @classmethod
    def dbname(cls, venueid):
        return "venue.%s" %(str(venueid))

    @classmethod
    def dbindex(cls):
        return "venues"

    @classmethod
    def create(cls, db, venueid, description, latitude, longitude):
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
        venue._playlist = playlist.Playlist.find(db, venueid)

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

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        raise NotImplementedError

    def count(self):
        """
        Returns the number of the users currently in the venue.
        """
        raise NotImplementedError

    def overall_mood(self):
        """
        Returns the overall combined mood of all the users in the venue.
        A positive value indicates a good mood.
        A negative value indicates a bad mood.
        The greater the value, the stronger the feeling.
        """
        raise NotImplementedError

    def checkin(self, userid):
        """
        Register an user in the venue. The user will now contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError

    def checkout(self, userid):
        """
        Deregister an user from the venue. The user will no longer contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError

    def playlist(self, num=1):
        """
        Returns a list of the last num played song.
        The currently played song is always the first one, the others
        following in reverse played order.
        """
        raise NotImplementedError

    def play(self, song):
        """
        Registers the given song as the one currently being played.
        """
        raise NotImplementedError

    def users(self):
        """
        Returns an iterable containing of all the users objects currently in the venue.
        """
        raise NotImplementedError

