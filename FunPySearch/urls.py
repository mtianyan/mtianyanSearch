"""FunPySearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from search.views import IndexView, SearchSuggest, SearchView, favicon_view
from user.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('favicon.ico', favicon_view),
    re_path('media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('', IndexView.as_view(), name="index"),
    path('suggest/', SearchSuggest.as_view(), name="suggest"),
    path('search/', SearchView.as_view(), name="search"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
