# part of moodeque

from moodeque.models import rediscoll
from moodeque.models import BaseModel
from moodeque.models import RedisModel


class Playlist(BaseModel, RedisModel):
    export_attrs = ()

    db_attrs = ()

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
        return song in self._songs

    def append(self, song):
        return self._songs.append(song)

    def current(self):
        return self._songs[-1]

    def clean(self):
        pass

    def __getitem__(self, index):
        return self._songs[index]

