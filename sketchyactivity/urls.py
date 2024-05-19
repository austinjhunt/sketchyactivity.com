from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as authtokenviews

# Django Rest Framework
router = routers.DefaultRouter()
router.register(r'meta', views.MetaStuffView, 'meta')
router.register(r'user', views.UserProfileView, 'user')
router.register(r'price', views.PriceView, 'price')
router.register(r'size', views.UniqueCommissionSizesView, 'size')


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('commission-prices/', views.CommissionsView.as_view(), name='commissions-prices'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('portfolio/', views.ListPortfolioItemsView.as_view(), name='portfolio'),
    path('', include(router.urls)),

    path('media/<slug:path>/<slug:filename>', views.media, name='media'),
    path('notify', views.NotifyView.as_view(), name='notify'),

#   path('upload', views.upload, name='upload'),
#     path('signup', views.site_signup, name='signup'),
#     path('logout', views.site_logout, name='logout'),
#     path('login', views.site_login, name='login'),
#     path('update_profile', views.update_profile, name='update-profile'),
#     path('update_profile_image', views.update_profile_image,
#          name='update-profile-image'),
#     path('pitem/<slug:pk>/edit', views.PortfolioItemEdit.as_view(),
#          name='portfolio-item-edit'),
#     path('pitem/<slug:pk>/delete', views.PortfolioItemDelete.as_view(),
#          name='portfolio-item-delete'),
#     path('pitem/<slug:id>', views.portfolio_item, name='portfolio-item'),
#     path('portfolio/manage', views.PortfolioManage.as_view(),
#          name='portfolio-manage'),
]
