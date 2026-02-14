from django.views.generic import ListView, DetailView
from .models import Category, LivestockItem

class LivestockListView(ListView):
    model = LivestockItem
    template_name = "livestock/list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all().prefetch_related("media", "items")
        return context

class LivestockDetailView(DetailView):
    model = LivestockItem
    template_name = "livestock/detail.html"
    context_object_name = "item"
