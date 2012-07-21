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

class BaseModel(object):
    export_attrs = ()

    def to_dict(self):
        return { attr: getattr(self, attr) for attr in self.export_attrs }


class RedisModel(object):
    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" %(cls.dbindex()))

    @classmethod
    def create(cls, db, **kwargs):
        did = cls.autoid(db)
        obj = cls.__new__(cls)
        obj.__init__(db, did, **kwargs)
        idx = rediscoll.Set(cls.dbindex(), db)
        idx.add(cls.dbname(did))
        obj.save()
        return obj

    @classmethod
    def find(cls, db, did):
        robj = rediscoll.Hash(cls.dbname(did), db)
        obj = cls.__new__(cls)
        obj.__init__(db, did, **robj)
        return obj

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(cls.dbindex(), db)
        return robj.all()

    def __init__(self, db, rid, **kwargs):
        self._db = db
        self._id = rid
        for k, v in kwargs:
            setattr(self, k, v)

    def save(self):
        robj = rediscoll.Hash(self.__class__.dbname(self._id), self._db)
        for attr in self.db_attrs:
            robj[attr] = getattr(self, attr)

    def destroy(self):
        idx = rediscoll.Set(self.__class__.dbindex(), self._db)
        idx.remove(self._id)
        self._db.delete(self.__class__.dbname(self._id))

