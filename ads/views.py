from django.shortcuts import render
from django.views import generic
from .models import Ads
from .counter import Counter


def home_page(request):
    return render(request, "home.html")


class AdsListView(generic.ListView):
    model = Ads
    template_name = "home.html"


class AdsDetailView(generic.DetailView):
    model = Ads
    template_name = "ads_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AdsDetailView, self).get_context_data(**kwargs)
        counter_view = Counter(AdsDetailView.__name__, self.object.pk)
        context["view_count"] = counter_view.hitcount()
        return context
