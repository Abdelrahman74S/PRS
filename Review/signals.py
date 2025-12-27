# product/signals.py
from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Review , Product , Category
from django.core.cache import cache

# send Email
@receiver(post_save, sender=Review)
def send_email_on_review_creation(sender, instance, created, **kwargs):
    if created:
        review = instance
        product_owner = review.product.user 
        reviewer = review.user
        
        subject = f"New Review on your product: {review.product.name}"
        message = f"Hello {product_owner.username},\n\n{reviewer.username} just reviewed your product.\nRating: {review.rating}/5\nComment: {review.comment}"
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [product_owner.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            
# caching
@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    print("Clearing product cache...")
    cache.delete_pattern('*product_list*')    
            
@receiver([post_save, post_delete], sender=Category)
def invalidate_category_cache(sender, instance, **kwargs):
    print("Clearing category cache...")
    cache.delete_pattern('*category_list*')           
    
@receiver([post_save, post_delete], sender=Review)
def invalidate_review_cache(sender, instance, **kwargs):
    print("Clearing review AND product cache...")
    
    cache.delete_pattern('*Review_list*')   
    
    cache.delete_pattern('*product_list*')          
    
