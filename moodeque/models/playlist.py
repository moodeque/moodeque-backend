# part of moodeque

import pickle
from . import rediscoll
from moodeque.models.base import BaseModel
from moodeque.models.base import RedisModel


class Playlist(RedisModel):
    db_attrs = ()

    @classmethod
    def register(cls, db, did):
        pass

    @classmethod
    def deregister(cls, db, did):
        pass

    @classmethod
    def all(cls, db):
        return ()

    @classmethod
    def load(cls, db, did):
        return {}

    @classmethod
    def dbname(cls, plid):
        return "playlist.%s" %(str(plid))

    @classmethod
    def dbindex(cls):
        return "playlists"

    def save(self):
        pass

    def __init__(self, db, plid):
        super(Playlist, self).__init__(db, plid)
        self.plid = plid
        self._songs = rediscoll.List(Playlist.dbname(plid), db)

    def __len__(self):
        return len(self._songs)

    def __contains__(self, song):
        _s = pickle.dumps(song)
        return _s in self._songs

    def append(self, song):
        return self._songs.append(pickle.dumps(song))

    @property
    def playing(self):
        return self.current()

    def current(self):
        return self._songs[-1]

    def clean(self):
        pass

    def __getitem__(self, index):
        return pickle.loads(self._songs[index])

