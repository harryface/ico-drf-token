from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator

from rest_framework import exceptions, permissions, response
from rest_framework.views import APIView

from ico_crypcentra.decorators import pass_if_window_allows
from .models import CustomUser, SiteConfiguration
from .authentication import JWTAuthentication
from .serializers import BidSerializer, ExternalBidPopulateSerializer, UserSerializer


class HomeView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['site_conf'] = SiteConfiguration.objects.all().first()
        return context


class RegisterAPIView(APIView):
    '''View for registration'''

    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.ValidationError(_('Passwords do not match!'))

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class LoginAPIView(APIView):
    '''View for logging in'''

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed(_('User not found!'))

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(_('Incorrect Password!'))

        token = JWTAuthentication.generate_jwt(user.id)

        response_ = response.Response()
        response_.set_cookie(key='jwt', value=token, httponly=True)
        response_.data = {
            'message': 'success'
        }

        return response_


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, _):
        response_ = response.Response()
        response_.delete_cookie(key='jwt')
        response_.data = {
            'message': 'success'
        }
        return response_


class UserDetailAPIView(APIView):
    '''A view for getting the user data'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data

        return response.Response(data)


class BidAPIView(APIView):
    '''View for Bidding'''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator([pass_if_window_allows, ], name='dispatch')
    def post(self, request):
        data = request.data

        serializer = BidSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return response.Response(serializer.data)


class ExternalBidPopulationAPIView(APIView):
    '''View for populating our bidding table '''

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @method_decorator([pass_if_window_allows, ], name='dispatch')
    def post(self, request):
        data = request.data

        serializer = ExternalBidPopulateSerializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)
