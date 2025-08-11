from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('mainpage:recommendations_by_category', args=[self.slug])

    def __str__(self):
        return self.name

class Post(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    product = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', null=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,
                                max_digits=10)
    quantity = models.IntegerField()
    avaible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product

    def get_absolute_url(self):
        return reverse('blog:postdetail', args=[self.id, self.slug])   