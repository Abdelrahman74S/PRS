from django.apps import AppConfig


class ReviewConfig(AppConfig):
    name = 'Review'
    
    def ready(self):
        import Review.signals  