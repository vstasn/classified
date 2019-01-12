from django.conf import settings
from redis import Redis

connect = Redis.from_url(settings.REDIS_URL)


class Counter:
    """
    Counter can count any view, using prefix redis_key
    """

    def __init__(self, prefix, hitkey):
        self.connect = connect
        self.counter_key = f"{prefix}:{hitkey}"

    def hit(self, request):
        if self._check_user(request):
            self.connect.incr(self.counter_key)

    def hitcount(self):
        return int(self.connect.get(self.counter_key))

    def _check_user(self, request):
        if request.session.session_key is None:
            request.session.save()
        session_prefix = self._check_user_key("session")
        if self.connect.sismember(session_prefix, request.session.session_key):
            return False

        if request.user.is_authenticated:
            user_prefix = self._check_user_key("user")
            if self.connect.sismember(user_prefix, request.user.id):
                return False
            self.connect.sadd(user_prefix, request.user.id)

        self.connect.sadd(session_prefix, request.session.session_key)

        return True

    def _check_user_key(self, user_prefix):
        return f"{self.counter_key}:{user_prefix}"
