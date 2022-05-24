import django_filters
from App_Accounts.models import *


class Donerfilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields=['city','bloodgroup','gender','religion']