import django_filters

from filter_page.models import App


class AppFilter(django_filters.FilterSet):
    name_app = django_filters.CharFilter(lookup_expr='icontains')
    company = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    release__gt = django_filters.NumberFilter(field_name='release', lookup_expr='year__gte')
    release__lt = django_filters.NumberFilter(field_name='release', lookup_expr='year__lte')

    def __len__(self):
        return len(self.qs)
