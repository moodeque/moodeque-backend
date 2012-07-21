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


from . import rediscoll
from . import playlist



class Venue(object):
    """
    This class represents a Moodeque venue.
    A Venue is any place where music is played, users gather and they (hopefully)
    have fun and interact.
    """
    def __init__(self, name, description, location, db):
        self._name = name
        self._description = description
        self._location = location
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
        return len(self._population)

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

    def playing(self, song):
        """
        Registers the given song as the one currently being played.
        """
        raise NotImplementedError

