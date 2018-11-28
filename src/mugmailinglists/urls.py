"""mugmailinglists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(
        url=reverse_lazy('list_index'),
        permanent=True)),
    url(r'^postorius/', include('postorius.urls')),
    url(r'^hyperkitty/', include('hyperkitty.urls')),
    url(r'', include('django_mailman3.urls')),
    url(r'^accounts/', include('allauth.urls')),
    # Django admin
    url(r'^admin/', admin.site.urls),
]
