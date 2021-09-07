from django.views import generic
from django.utils.translation import ugettext_lazy as _

from rest_framework.views import APIView


class HomeView(generic.TemplateView):
    pass


class RegisterAPIView(APIView):
    pass


class LoginAPIView(APIView):
    pass


class LogoutAPIView(APIView):
    pass


class UserDetailAPIView(APIView):
    pass


class BidAPIView(APIView):
    pass


class ExternalBidPopulationAPIView(APIView):
    pass
