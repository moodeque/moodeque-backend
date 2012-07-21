from . import rediscoll


class BaseModel(object):
    export_attrs = ()

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.export_attrs}


class RedisModel(object):
    @classmethod
    def autoid(cls, db):
        return db.incr("%s.seqno" % (cls.dbindex()))

    @classmethod
    def register(cls, db, did):
        idx = rediscoll.Set(cls.dbindex(), db)
        idx.add(cls.dbname(did))

    @classmethod
    def deregister(cls, db, did):
        idx = rediscoll.Set(cls.dbindex(), db)
        idx.remove(did)

    @classmethod
    def all(cls, db):
        robj = rediscoll.Set(cls.dbindex(), db)
        return robj.all()

    @classmethod
    def create(cls, db, **kwargs):
        did = cls.autoid(db)
        obj = cls.__new__(cls)
        obj.__init__(db, did, **kwargs)
        cls.register(db, did)
        obj.save()
        return obj

    @classmethod
    def load(cls, db, did):
        return rediscoll.Hash(cls.dbname(did), db)

    @classmethod
    def find(cls, db, did):
        robj = cls.load(db, did)
        obj = cls.__new__(cls)
        obj.__init__(db, did, **robj)
        return obj

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
        self.__class__.deregister(self._db, self._id)
        self._db.delete(self.__class__.dbname(self._id))

