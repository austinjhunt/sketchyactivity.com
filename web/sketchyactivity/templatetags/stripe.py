from django import template
register = template.Library()
def convert_stripe_price_to_userfriendly_price(price):
    """ stripe expects everything to be in cents; to avoid
    the user seeing a $75 charge as $7500, convert by dividing by 100 """
    return int(price) / 100

register.filter('convert_stripe_price_to_userfriendly_price',convert_stripe_price_to_userfriendly_price)