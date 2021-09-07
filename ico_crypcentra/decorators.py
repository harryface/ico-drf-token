from functools import wraps
from main.models import SiteConfiguration
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions


def pass_if_window_allows(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        conf = SiteConfiguration.objects.all().first()
        if not conf or not conf.is_within_window:        
            raise exceptions.ValidationError(_('The bidding window has closed!'))
        else:
            return function(request, *args, **kwargs)

    return wrap
