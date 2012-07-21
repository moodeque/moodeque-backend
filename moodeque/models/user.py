# part of moodeque

from moodeque.models import rediscoll
from moodeque.models import BaseModel
from moodeque.models import RedisModel


class User(BaseModel, RedisModel):
    export_attrs = ('mood',)

    db_attrs = ('mood',)

    @classmethod
    def dbname(cls, userid):
        return "user.%s" %(str(userid))

    @classmethod
    def dbindex(cls):
        return "users"

    def __init__(self, db, userid, **kwargs):
        super(User, self).__init__(db, plid)
        self.userid = userid

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


