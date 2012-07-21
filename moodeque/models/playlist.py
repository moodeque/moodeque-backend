
from moodeque.models import rediscoll


class PlayList(object):
    @classmethod
    def dbname(cls, plid):
        return "playlist.%s" %(str(plid))

    @classmethod
    def dbindex(cls):
        return "playlists"

    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" %(PlayList.dbindex()))

    @classmethod
    def create(cls, db):
        plid = PlayList.autoid(db)
        pl = PlayList(db, plid)
        idx = rediscoll.Set(PlayList.dbindex(), db)
        idx.add(PlayList.dbname(plid))
        pl.save()
        return pl

    @classmethod
    def find(cls, db, plid):
        return rediscoll.List(PlayList.dbname(plid), db)

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(PlayList.dbindex(), db)
        return robj.all()

    def save(self):
        pass

    def destroy(self):
        idx = rediscoll.Set(PlayList.dbindex(), self._db)
        idx.remove(self.plid)
        self._db.delete(PlayList.dbname(self.plid))

    def __init__(self, db, plid):
        self.plid = plid
        self._songs = rediscoll.List(PlayList.dbname(plid), db)

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

