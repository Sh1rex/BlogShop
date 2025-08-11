from django.db import models
from django.conf import settings 
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    profileimg = models.ImageField(upload_to='avatars/', blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Subscription(models.Model):
    subscriber  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriber')
    subscribed_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscribed_to')
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'subscribed_to'], name='unique_subscription')
        ]