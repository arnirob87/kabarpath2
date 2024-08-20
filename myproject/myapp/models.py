from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# class User(AbstractUser):
#     phone_number = models.CharField(max_length=15, unique=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     referral_id = models.CharField(max_length=15, blank=True, null=True)
#     level = models.IntegerField(default=1)
#     points = models.IntegerField(default=0)
    

#     def save(self, *args, **kwargs):
#         if not self.referral_id:
#             self.referral_id = self.phone_number
#         super().save(*args, **kwargs)

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    referral_id = models.CharField(max_length=100, blank=True, null=True)
    level = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    can_create_post = models.BooleanField(default=False)
    can_create_product = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.referral_id:
            self.referral_id = self.phone_number
        super().save(*args, **kwargs)

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1500, blank=True, null=True)
    duration = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_pic1 = models.ImageField(upload_to='product_pics/')
    product_pic2 = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    product_pic3 = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    product_pic4 = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    thumb = models.ImageField(upload_to='product_pics/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.user.username} for {self.product.name}"



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', blank=True, null=True)
    content = RichTextUploadingField(default='')
    image1 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    @property
    def total_likes(self):
        return self.likes.count()
    

# Like Model
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    


class Withdrawal(models.Model):
    STATUS_CHOICES = (
        (True, 'Processed'),
        (False, 'Pending'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    money_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.user.username} - {self.money_amount} - {"Processed" if self.is_processed else "Pending"}'
    
class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)