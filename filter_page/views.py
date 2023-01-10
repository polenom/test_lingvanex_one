from django.shortcuts import render
from django.views.generic import ListView

from filter_page.filter import AppFilter
from filter_page.models import App
from filter_page.utils import ValueFilter


# Create your views here.
class Filter(ListView):
    template_name = 'base.html'
    paginate_by = 10
    filters = None
    def get_queryset(self):
        filters = ValueFilter(self.request, queryset=App.objects.all())
        queryset = filters.sorted()
        self.filters = filters.get_value()
        return AppFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data( *args, **kwargs)
        # context['filter_form'] = AppFilter(self.request.GET)
        return context