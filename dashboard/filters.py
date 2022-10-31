import django_filters
from myadmin.models import Policy
from django_filters import DateFilter


class PolicyFilter(django_filters.FilterSet):
    start_date=DateFilter(field_name="date_created",lookup_expr='gte')
    end_date=DateFilter(field_name="date_created",lookup_expr='lte')

    class Meta:
        model = Policy
        fields = '__all__'
        exclude = ['user','date_created']
