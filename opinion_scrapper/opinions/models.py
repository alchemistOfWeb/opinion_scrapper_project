from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self) -> str:
        return self.url


class Opinion(models.Model):
    USING_DURATION_CHOICES = (
        ('a', "менее месяца"),
        ('b', "не более года"),
        ('c', "более года"),
    )

    author_name = models.CharField(max_length=255)
    comments_num = models.IntegerField()
    stars_num = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    source = models.URLField()
    using_duration = models.CharField(
        max_length=255, choices=USING_DURATION_CHOICES)
    advantages = models.TextField(max_length=3000, blank=True)
    disadvantages = models.TextField(max_length=3000, blank=True)
    content = models.TextField(max_length=3000, blank=True)

    product = models.ForeignKey(
        Product, related_name='opinions', on_delete=models.CASCADE)

    # def product_url(self):
    #     return self.product.url
    # product_url.short_description = 'product url'

    # def product_title(self):
    #     return self.product.title
    # product_title.short_description = 'product title'


    def __str__(self) -> str:
        return self.author_name

# class DurationChoice(models.Model):
#     title = CharField(max_lenthg=255)
