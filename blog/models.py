from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


User = get_user_model()


class Article(models.Model):
    STATUS = (
        ('draft','Draft'),
        ('publish', 'Publish')
    )
    user = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = RichTextField()
    image = models.ImageField(upload_to='articles/')
    status = models.CharField(choices=STATUS , max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    numbers_rating = models.FloatField(default=0)
    total_rates = models.PositiveBigIntegerField(default=0)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0)

    tags = TaggableManager()

    @property
    def get_tags(self):
        return self.tags.all()