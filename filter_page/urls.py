from django.urls import path, include
from filter_page.views import Filter

urlpatterns = [
    path('', Filter.as_view(), name='main')
]
