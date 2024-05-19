
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from ..serializers import *
from rest_framework.response import Response



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
