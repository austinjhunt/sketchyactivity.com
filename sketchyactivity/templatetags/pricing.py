from django import template
import datetime
from ..models import Price
register = template.Library()



def on_sale(price, sale_amount):
    """ sale amount expressed as decimal, e.g. 0.4, for 40% off """
    return round(price * (1 - sale_amount), 2)

def get_traditional_price(size, num_subjects):
    return round(Price.objects.get(style='TR', size=size, num_subjects=num_subjects).amount, 2)

def get_digital_price(num_subjects):
    return round(Price.objects.get(style='DI', num_subjects=num_subjects).amount, 2)

def to_pretty_percent(decimal_sale):
    return f'{decimal_sale * 100}%'


register.filter('on_sale', on_sale)
register.filter('get_traditional_price', get_traditional_price)
register.filter('get_digital_price', get_digital_price)
register.filter('to_pretty_percent', to_pretty_percent)