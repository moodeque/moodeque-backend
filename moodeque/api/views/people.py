from moodeque.api.views import (BaseView,
                                MatchBaseView)
from pyramid.view import (view_defaults,
                          view_config)
from moodeque.models import User

class PersonBase(MatchBaseView):

    def __init__(self, request):
        super(PersonBase, self).__init__(request)
        self.user = User.find_by_name(self.request.db, self.uid)


@view_defaults(route_name="people")
class PeopleView(BaseView):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        users = [u.to_dict() for u in User.all(self.request.db)]
        return {"users": users}

    def post(self):
        user = User.create(name=self.request.params['name'],
                           mood=self.request.params.get('mood', 0))
        return user.to_dict()


@view_defaults(route_name="person")
class PersonView(PersonBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def get(self):
        return self.user.to_dict()

    def put(self):
        if 'mood' in self.request.params:
            self.user.mood = self.request.params['mood']
            self.log.info("Updated user: {0}".format(self.user))
            self.user.save()
        return self.user.to_dict()

    def delete(self):
        self.user.destroy()
        return self.user.to_dict()


@view_defaults(route_name="login")
class LoginView(PersonBase):

    @view_config(renderer='json')
    def dispatch(self):
        return self._dispatch()

    def post(self):
        message = "User {0} logged in".format(self.uid)
        User.create(self.request.db, name=self.uid, mood=0)
        self.log.info(message)
        return {}
