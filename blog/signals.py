from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Article


@receiver(post_save, sender=Article)
def create_profile(sender,  **kwargs):
    cache.clear()


@receiver(post_delete, sender=Article)
def create_profile(sender,  **kwargs):
    cache.clear()