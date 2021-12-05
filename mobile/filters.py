import django_filters
from mobile.models import Mobile

class MobileFilter(django_filters.FilterSet):
    class Meta:
        model=Mobile
        fields=["mobile_name","price","copies","colour","storage"]
