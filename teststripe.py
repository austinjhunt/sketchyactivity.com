from sketchyactivity.models import *
from django.contrib.auth.models import User
def main():
    """ I want to add some very cheap items to my Profile cart
    and then check out to test the stripe integration """
    profile = UserProfile.objects.get(user=User.objects.get(username='huntaj@cofc.edu'))
    cart = profile.cart
    print(cart.all())
    # add a fake item if not exists
    test_products = Product.objects.filter(name='test')
    if test_products.count() == 0:
        # create a fake $1 product
        p = Product(
            name='test',
            description='fake product to test stripe integration',
            type='test product',
            price=1)
        p.save()
    else:
        p = test_products[0]
    # add product to my cart
    cart.add(p)
    # save profile
    profile.save()

# after running this script with
# python manage.py shell < test-cart-items.py,
# go load the checkout page in dev and submit a payment
if __name__ == "__main__":
    main()