# (C) 2012 Francesco Romani <fromani . gmail . com>
from moodeque.models import rediscoll


class User(object):
    @classmethod
    def dbname(cls, userid):
        return "user.%s" %(str(userid))

    @classmethod
    def dbindex(cls):
        return "users"

    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" %(Playlist.dbindex()))

    @classmethod
    def create(cls, db, mood):
        userid = User.autoid(db)
        usr = User(db, userid, mood)
        idx = rediscoll.Set(User.dbindex(), db)
        idx.add(User.dbname(userid))
        usr.save()
        return usr

    @classmethod
    def find(cls, db, userid):
        robj = rediscoll.Hash(User.dbname(userid), db)
        return User(db, userid, robj['mood'])

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(User.dbindex(), db)
        return robj.all()

    def save(self):
        robj = rediscoll.Hash(User.dbname(self.userid), self._db)
        robj['mood'] = self.mood

    def destroy(self):
        idx = rediscoll.Set(User.dbindex(), self._db)
        idx.remove(self.userid)
        self._db.delete(User.dbname(self.userid))

    def __init__(self, db, userid, mood):
        self._db = db
        self.userid = userid
        self.mood = mood

    def checkin(self, venue):
        """
        Register an user in the venue. The user will now contribute to
        the overall mood of the venue.
        """
        venue.checkin(self)

    def checkout(self, venue):
        """
        Deregister an user from the venue. The user will no longer contribute to
        the overall mood of the venue.
        """
        venue.checkout(self)


