import django_filters
from accounts.models import User


class UserSearchFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    fullname = django_filters.CharFilter(field_name='fullname', lookup_expr='icontains')
    
    class Meta:
        model = User
        fields = []