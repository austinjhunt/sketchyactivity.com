from django.urls import path
from django.views.static import serve
from django.conf.urls import url
from . import views
from django.conf import settings
urlpatterns = [
    path('', views.index),
    path('media/<slug:path>/<slug:filename>', views.media),
    path('commissions', views.CommissionsView.as_view()),
    path('notify', views.notify),
    path('delete', views.delete),
    path('upload', views.upload),
    path('logout', views.site_logout),
    path('login', views.site_login),
    path('signup', views.site_signup),
    path('messaging',views.slack_msging_endpoint), # messaging endpoint for slack api
    path('messaging/(\d+)', views.messaging), # slack_msging_endpoint function filters out the user id then calls this function to direct response to correct user.
    path('update_profile', views.update_profile),
    path('pitem/<slug:id>', views.portfolio_item)
]
if settings.DEBUG:
    urlpatterns +=  [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]