from django.core.cache import cache
from django.conf import settings
import graphene
from .types import ProductType
from .models import Product


class FilterByInput(graphene.InputObjectType):
    available = graphene.Boolean(required=False)
    special_offer = graphene.Boolean(required=False)
    category = graphene.String(required=False)


class ProductQuery(graphene.ObjectType):
    products = graphene.List(ProductType,
        skip=graphene.Int(required=False),
        limit=graphene.Int(required=False),
        filter_by=FilterByInput(required=False),
        order_by=graphene.String(required=False))
    product = graphene.Field(ProductType,id=graphene.ID())

    def resolve_products(parent, info, skip=None, limit=None, filter_by=None, order_by=None):
        query = None
        # get the products from cache
        if 'products' in cache:
            query=cache.get('products')
        else:
            query = Product.objects.all()
            cache.set('products',query,timeout=settings.CACHE_TIMEOUT_PRODUCTS )
        
        if skip != None:
            query = query[skip:]
        
        if limit != None:
            query = query[:limit]
        
        if filter_by != None:
            if filter_by.available != None :
                if filter_by.available:
                    query = query.filter(available=True)
                else:
                    query = query.filter(available=False)
            
            if filter_by.special_offer != None :
                if filter_by.special_offer:
                    query = query.filter(special_offer=True)
                else:
                    query = query.filter(special_offer=False)
            
            if filter_by.category != None :
                query = query.filter(category__name=filter_by.category)
        
        if order_by != None :
            query = query.order_by(order_by)
        
        return query
    
    def resolve_product(parent, info, id):
        try:
            query = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None
        
        return query