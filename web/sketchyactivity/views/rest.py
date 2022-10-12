from ..models import PortfolioItem
from .s3 import s3_client
from .util import update_private_video_url, update_private_urls_full_portfolio
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers import *
from rest_framework.response import Response
from django.core.cache import cache


def get_updated_portfolio(limit=None):
    portfolio = PortfolioItem.objects.all().order_by('-date')
    if limit:
        portfolio = portfolio[:int(limit)]
    # update private urls if they need to be updated
    if not cache.get('updated_private_video_url'):
        private_video_url = update_private_video_url(s3_client)
        # half the max expiration time of the private urls for the media files in s3.
        cache.set('updated_private_video_url',
                  private_video_url, timeout=302400)
    if not cache.get('updated_private_urls'):
        print("Updating private urls for portfolio...")
        update_private_urls_full_portfolio(portfolio, s3_client)
        print("Setting cache.updated_private_urls ")
        # half the max expiration time of the private urls for the media files in s3.
        cache.set('updated_private_urls', 'is_updated', timeout=302400)
    else:
        print("Cache updated_private_urls is set already")
    return portfolio


class PortfolioView(viewsets.ModelViewSet):
    serializer_class = PortfolioItemSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_updated_portfolio(
            limit=self.request.query_params.get('limit', None)
        )


class MetaStuffView(viewsets.ModelViewSet):
    serializer_class = MetaStuffSerializer
    queryset = MetaStuff.objects.all()
    permission_classes = [IsAdminUser]


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAdminUser]


class PriceView(viewsets.ModelViewSet):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()
    permission_classes = [IsAdminUser]


class UniqueCommissionSizesView(viewsets.ViewSet):
    serializer_class = PriceSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        prices = Price.objects.all()
        # traditional
        traditional_prices = prices.filter(style='TR')
        for p in traditional_prices:
            print(f'{p.style} - {p.amount} - {p.description}')
        unqiue_sizes = traditional_prices.order_by(
            'size').distinct().values_list('size', flat=True)
        unique_sizes = sorted(
            unqiue_sizes, key=lambda el: float(el.split('x')[0]))
        return Response(unique_sizes)
