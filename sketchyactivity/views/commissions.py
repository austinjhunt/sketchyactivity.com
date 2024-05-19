from rest_framework.views import APIView
from rest_framework.response import Response
from sketchyactivity.models import MetaStuff, Price

class CommissionsView(APIView):
    def get(self, request):
        ms = MetaStuff.objects.first()
        sale_active = ms.sale_still_active()
        digital_prices = []
        traditional_prices = []

        for traditional in Price.objects.filter(style='TR').order_by('size'):
            people_person_string = 'people' if traditional.num_subjects > 1 else 'person'
            amount = traditional.amount if not sale_active else ms.get_sale_price(original_price=traditional.amount)

            traditional_prices.append({
                'value': f'tr-{traditional.size}-{traditional.num_subjects}',
                'display_name': f'Ballpoint Pen | {traditional.size} | {traditional.num_subjects} {people_person_string} | ${amount}'
            })

        for digital in Price.objects.filter(style='DI').order_by('num_subjects'):
            people_person_string = 'people' if digital.num_subjects > 1 else 'person'
            amount = digital.amount if not sale_active else ms.get_sale_price(original_price=digital.amount)

            digital_prices.append({
                'value': f'di-{digital.num_subjects}',
                'display_name': f'Digital | {digital.num_subjects} {people_person_string} | ${amount}'
            })

        return Response({
            'traditional_prices': traditional_prices,
            'digital_prices': digital_prices,
            'sale': {
                'active': sale_active,
                'amount': ms.sale_amount
                }
        }, status=200)
