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
from moodeque.models import venue


class User(object):
    @classmethod
    def dbname(cls, userid):
        return "user.%s" %(str(userid))

    @classmethod
    def dbindex(cls):
        return "users"

    @classmethod
    def create(cls, db, userid, mood):
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

    def checkin(self, venueid):
        """
        Register an user in the venue. The user will now contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError

    def checkout(self, venueid):
        """
        Deregister an user from the venue. The user will no longer contribute to
        the overall mood of the venue.
        """
        raise NotImplementedError


