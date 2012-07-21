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

