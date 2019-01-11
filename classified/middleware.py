from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from ads.counter import Counter


class CounterMiddleware(MiddlewareMixin):
    """ Middleware for count uri visits. """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Possible to count any view, need to update settings
        """
        if view_func.__name__ == settings.COUNTER_ADS_VIEW:
            counter_key = view_kwargs.get("pk")
            ads_counter = Counter(view_func.__name__, counter_key)
            ads_counter.hit(request)
