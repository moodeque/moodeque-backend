# part of moodeque

from . import rediscoll
from moodeque.models.base import BaseModel
from moodeque.models.base import RedisModel


class Crowd(RedisModel):
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
    def dbname(cls, crid):
        return "crowd.%s" %(str(crid))

    @classmethod
    def dbindex(cls):
        return "crowds"

    def save(self):
        pass

    def __init__(self, db, crid):
        super(Crowd, self).__init__(db, crid)
        self.crid = crid
        self._people = rediscoll.Set(Crowd.dbname(crid), db)

    def __len__(self):
        return len(self._people)

    def __contains__(self, soul):
        return soul in self._people

    def all(self):
        return self._people.members

    def add(self, soul):
        return self._people.add(soul)

    def remove(self, soul):
        return self._people.remove(soul)

    def clean(self):
        pass

