"""myproject URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from sketchyactivity import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^notify/$', views.notify),
    url(r'^delete/$', views.delete),
    url(r'^upload/$', views.upload),
    url(r'^logout/$', views.site_logout),
    url(r'^login/$', views.site_login),
    url(r'^signup/$', views.site_signup),
    url(r'^messaging/$',views.slack_msging_endpoint), # messaging endpoint for slack api
    url(r'^messaging/(\d+)/$', views.messaging), # slack_msging_endpoint function filters out the user id then calls this function to direct response to correct user.
    path('admin/', admin.site.urls),
    url(r'^update_profile/', views.update_profile),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


