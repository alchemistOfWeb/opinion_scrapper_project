from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()


class Opinion(models.Model):
    author = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='opinions', on_delete=models.CASCADE)
    comments_num = models.IntegerField()
    stars = models.SmallIntegerField() # google: max value for integer field
    source = models.CharField(max_length=255)
    # google: dataRange field or DurationField
    using_during = models.DurationField()
    advantages = models.TextField(max_length=1024) # seek out in the site
    disadvantages = models.TextField(max_length=1024) # seek out in the site
    content = models.TextField(max_length=1024) # seek out in the site


    def __str__(self) -> str:
        return self.title
