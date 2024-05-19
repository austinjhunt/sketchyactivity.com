import logging

from rest_framework.views import APIView, Response
from django.core.cache import cache
from ..models import PortfolioItem
from .s3 import s3_client
from .util import update_private_video_url, update_private_urls_full_portfolio
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logger = logging.getLogger('sketchyactivity')

class ListPortfolioItemsView(APIView):


    def get_updated_portfolio(self, page=1, items_per_page=21):
        logger.info({
            'action': 'ListPortfolioItemsView.get_updated_portfolio',
            'page': page,
            'items_per_page': items_per_page,
        })
        try:
            portfolio = PortfolioItem.objects.all().order_by('-date')
            paginator = Paginator(portfolio, items_per_page)
            portfolio_page = paginator.get_page(page)
            logger.info({
                'action': 'get_updated_portfolio',
                'portfolio_length': len(portfolio_page),
            })
            # update private urls if they need to be updated
            if not cache.get('updated_private_video_url'):
                private_video_url = update_private_video_url(s3_client)
                # half the max expiration time of the private urls for the media files in s3.
                cache.set('updated_private_video_url',
                        private_video_url, timeout=302400)
            if not cache.get('updated_private_urls'):
                logger.info({
                    'action': 'get_updated_portfolio',
                    'message': 'Updating private urls for portfolio items',
                })
                update_private_urls_full_portfolio(portfolio_page, s3_client)
                # half the max expiration time of the private urls for the media files in s3.
                cache.set('updated_private_urls', 'is_updated', timeout=302400)
            else:
                logger.info({
                    'action': 'get_updated_portfolio',
                    'message': 'Private urls for portfolio items are already updated',
                })
            return portfolio_page
        except Exception as e:
            logger.error({
                'action': 'get_updated_portfolio',
                'error': str(e),
            })
            return []

    def get(self, request):
        items_per_page = self.request.query_params.get('items_per_page', 21)
        page = self.request.query_params.get('page', 1)
        logger.info(
            {
                'action': 'ListPortfolioItemsView.get',
                'items_per_page': items_per_page,
                'page': page
            }
        )
        portfolio = self.get_updated_portfolio(page, items_per_page)
        portfolio = [p.format_json() for p in portfolio]
        return Response(
            {
                'portfolio': portfolio,
            },
            status=200
        )
