from django.core.cache import cache
from django.conf import settings
import graphene
from .types import Category, CategoryType
from .models import Category


class CategoriesQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(parent, info):
        query = None
        if 'categories' in cache:
            query = cache.get('categories')
        else:
            query=Category.objects.all()
            cache.set('categories',query,timeout=settings.CACHE_TIMEOUT_CATEGORY)

        return query