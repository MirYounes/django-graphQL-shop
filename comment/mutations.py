import graphene
from graphene.types.generic import GenericScalar
from products.models import Product
from blog.models import Article
from .models import Comment


class CommentInput(graphene.InputObjectType):
    rate = graphene.Int(required=True)
    object_id = graphene.ID(required=True)
    body = graphene.String(required=True)
    fullname = graphene.String(required=True)


class CommentToProduct(graphene.Mutation):
    class Arguments:
        data=CommentInput(required=True)

    response = GenericScalar()

    def mutate(parent, info, data):
        # get the product
        try:
            product = Product.objects.get(id=data.object_id)
        except:
            return CommentToProduct(
                response={"ok":False,"message":"product does not exist"})
        
        Comment.objects.create(
            rate=data.rate,
            body=data.body,
            fullname=data.fullname,
            content_object=product
        )
        
        product.numbers_rating+=1
        product.total_rates+=data.rate
        product.rate = product.total_rates / product.numbers_rating
        product.save()

        return CommentToProduct(
            response={"ok":True,"message":"comment added"})


class CommentToArticle(graphene.Mutation):
    class Arguments:
        data=CommentInput(required=True)

    response = GenericScalar()

    def mutate(parent, info, data):
        # get the product
        try:
            article = Article.objects.get(id=data.object_id)
        except:
            return CommentToProduct(
                response={"ok":False,"message":"article does not exist"})
        
        Comment.objects.create(
            rate=data.rate,
            body=data.body,
            fullname=data.fullname,
            content_object=article
        )
        
        article.numbers_rating+=1
        article.total_rates+=data.rate
        article.rate = article.total_rates / article.numbers_rating
        article.save()

        return CommentToProduct(
            response={"ok":True,"message":"comment added"})


class AddReply(graphene.Mutation):
    class Arguments:
        data=CommentInput(required=True)

    response = GenericScalar()

    def mutate(parent, info, data):
        # get the comment
        try:
            comment = Comment.objects.get(id=data.object_id)
        except:
            return CommentToProduct(
                response={"ok":False,"message":"comment does not exist"})
        
        Comment.objects.create(
            rate=data.rate,
            body=data.body,
            fullname=data.fullname,
            content_object=comment
        )

        return CommentToProduct(
            response={"ok":True,"message":"comment added"})


class CommentMutation(graphene.ObjectType):
    comment_to_product = CommentToProduct.Field()
    comment_to_article = CommentToArticle.Field()
    add_reply = AddReply.Field()