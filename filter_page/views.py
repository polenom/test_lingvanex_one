from django.shortcuts import render
from django.views.generic import ListView

from filter_page.models import App


# Create your views here.
class Filter(ListView):
    model = App
    pa