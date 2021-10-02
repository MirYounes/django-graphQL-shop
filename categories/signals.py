from django.db.models.signals import post_save , post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category


@receiver(post_save, sender=Category)
def create_profile(sender,  **kwargs):
    cache.clear()


@receiver(post_delete, sender=Category)
def create_profile(sender,  **kwargs):
    cache.clear()