# part of moodeque

from . import rediscoll
from moodeque.models.base import (BaseModel,
                                  RedisModel)


class User(BaseModel, RedisModel):
    export_attrs = ('name', 'mood',)

    db_attrs = ('name', 'mood',)

    @classmethod
    def dbname(cls, userid):
        return "user.%s" %(str(userid))

    @classmethod
    def dbindex(cls):
        return "users"

    @classmethod
    def find_by_name(cls, db, name):
        for u in cls.all(db):
            if u.name == name:
                return u

    def __init__(self, db, userid, **kwargs):
        super(User, self).__init__(db, userid, **kwargs)
        self.userid = userid

    def __str__(self):
        return "%s (%i) has mood %i" %(self.name, int(self.userid), int(self.mood))
 
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


