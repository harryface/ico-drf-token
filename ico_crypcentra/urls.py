"""ico_crypcentra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import (BidAPIView, ExternalBidPopulationAPIView,
                    HomeView, RegisterAPIView, LoginAPIView,
                    LogoutAPIView, UserDetailAPIView
                )

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),

    path('user', UserDetailAPIView.as_view(), name='user'),
    path('', HomeView.as_view(), name='home'),
    
    path('bid', BidAPIView.as_view(), name='bid'),
    path('external/bid', ExternalBidPopulationAPIView.as_view(), name='external_bid'),

    path('admin/', admin.site.urls),
]
