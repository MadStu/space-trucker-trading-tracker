"""spacetrucker URL Configuration

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
from django.urls import path, include
from trading.views import index, editor, prices, usage, api_call
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('editor/', editor, name='editor'),
    path('prices/', prices, name='prices'),
    path('apicall/', api_call, name='api_call'),
    path('usage/', usage, name='usage'),
    path('accounts/', include('allauth.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')))
]

handler400 = 'trading.views.error_400'
handler403 = 'trading.views.error_403'
handler404 = 'trading.views.error_404'
handler500 = 'trading.views.error_500'
