# product/throttling.py
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review_create'

class ProductListThrottle(AnonRateThrottle):
    scope = 'product_list'