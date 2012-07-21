
from moodeque.models import rediscoll


class Playlist(object):
    @classmethod
    def dbname(cls, plid):
        return "playlist.%s" %(str(plid))

    @classmethod
    def dbindex(cls):
        return "playlists"

    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" %(Playlist.dbindex()))

    @classmethod
    def create(cls, db):
        plid = Playlist.autoid(db)
        pl = Playlist(db, plid)
        idx = rediscoll.Set(Playlist.dbindex(), db)
        idx.add(Playlist.dbname(plid))
        pl.save()
        return pl

    @classmethod
    def find(cls, db, plid):
        return rediscoll.List(Playlist.dbname(plid), db)

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(Playlist.dbindex(), db)
        return robj.all()

    def save(self):
        pass

    def destroy(self):
        idx = rediscoll.Set(Playlist.dbindex(), self._db)
        idx.remove(self.plid)
        self._db.delete(Playlist.dbname(self.plid))

    def __init__(self, db, plid):
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

