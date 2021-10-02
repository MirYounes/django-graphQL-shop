from django.db import models
from categories.models import Category
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from graphene_django.converter import convert_django_field
from graphene import String, List


@convert_django_field.register(TaggableManager)
def convert_field_to_string(field, registry=None):
    return List(String, source="get_tags")


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=5 , decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    color = models.ManyToManyField(Color)
    available = models.BooleanField(default=True)
    tags = TaggableManager()
    description = RichTextField()
    image = models.ImageField(upload_to='products/image/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    sale_number = models.PositiveBigIntegerField(default=0)
    special_offer = models.BooleanField(default=False)

    numbers_rating = models.FloatField(default=0)
    total_rates = models.PositiveBigIntegerField(default=0)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f'{self.title}-{self.id}'

    @property
    def get_tags(self):
        return self.tags.all()
    



class Gallery(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
    
