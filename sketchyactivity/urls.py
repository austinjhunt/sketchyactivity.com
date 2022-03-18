from django.urls import path
from django.views.static import serve
from django.conf.urls import url, include
from . import views
from django.conf import settings
from rest_framework import routers
from rest_framework.authtoken import views as authtokenviews


# Django Rest Framework
router = routers.DefaultRouter()
router.register(r'portfolio', views.PortfolioView, 'portfolio')
router.register(r'meta', views.MetaStuffView, 'meta')
router.register(r'user', views.UserProfileView, 'user')
router.register(r'price', views.PriceView, 'price')
router.register(r'size', views.UniqueCommissionSizesView, 'size')

urlpatterns = [
    path('', views.index, name='home'),
    # DRF
    path('api/', include(router.urls)),
    path('api/obtain-auth-token/', authtokenviews.obtain_auth_token),

    path('media/<slug:path>/<slug:filename>', views.media, name='media'),
    path('commissions', views.CommissionsView.as_view(),name='commissions'),
    path('about', views.AboutView.as_view(), name='about'),
    path('notify', views.notify,name='notify'),
    path('upload', views.upload,name='upload'),
    path('logout', views.site_logout,name='logout'),
    path('login', views.site_login,name='login'),
    path('signup', views.site_signup,name='signup'),
    path('messaging',views.slack_msging_endpoint,name='messaging-endpoint'), # messaging endpoint for slack api
    path('messaging/(\d+)', views.messaging,name='messaging'), # slack_msging_endpoint function filters out the user id then calls this function to direct response to correct user.
    path('update_profile', views.update_profile,name='update-profile'),
    path('pitem/<slug:pk>/edit', views.PortfolioItemEdit.as_view(), name='portfolio-item-edit'),
    path('pitem/<slug:pk>/delete', views.PortfolioItemDelete.as_view(), name='portfolio-item-delete'),
    path('pitem/<slug:id>', views.portfolio_item, name='portfolio-item'),
    path('portfolio/manage', views.PortfolioManage.as_view(), name='portfolio-manage'),
    url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]
