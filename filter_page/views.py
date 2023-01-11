from django.shortcuts import render
from django.views.generic import ListView

from filter_page.filter import AppFilter
from filter_page.models import App
from filter_page.utils import ValueFilter


# Create your views here.
class Filter(ListView):
    template_name = 'base.html'
    filters = None

    def get_queryset(self):
        filters = ValueFilter(self.request, queryset=App.objects.all())
        queryset = filters.get_qs()
        self.filters = filters.get_value()
        self.paginate_by = self.filters.get('page_elem')
        return AppFilter(self.filters, queryset=queryset).qs

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data( *args, **kwargs)
        context['filters'] = self.filters
        return context
