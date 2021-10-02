from django.core.cache import cache
from django.conf import settings
import graphene
from .types import ArticleType
from .models import Article


class BlogQuery(graphene.ObjectType):
    articles = graphene.List(ArticleType,
        skip=graphene.Int(required=False),
        limit=graphene.Int(required=False),
        order_by=graphene.String(required=False))
    article = graphene.Field(ArticleType,id=graphene.ID())

    def resolve_articles(parent, info, skip=None, limit=None, order_by=None):
        query = None
        # get the articles from cache
        if 'articles' in cache:
            query=cache.get('articles')
        else:
            query = Article.objects.all()
            cache.set('articles',query,timeout=settings.CACHE_TIMEOUT_ARTICLES )
        
        if skip != None:
            query = query[skip:]
        
        if limit != None:
            query = query[:limit]
        
        if order_by != None :
            query = query.order_by(order_by)
        
        return query
    
    def resolve_article(parent, info, id):
        try:
            query = Article.objects.get(id=id)
        except Article.DoesNotExist:
            return None
        
        return query