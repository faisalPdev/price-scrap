from django.db import models

# Create your models her
class searchHistory(models.Model):
    search_term = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True)
    flipkart_title=models.CharField(max_length=200)
    flipkart_price=models.CharField(max_length=100)
    amazon_title=models.CharField(max_length=200)
    amazon_price=models.CharField(max_length=100)
    croma_title=models.CharField(max_length=200)
    croma_price=models.CharField(max_length=100)
    gadget_title=models.CharField(max_length=200)
    gadget_price=models.CharField(max_length=100)
    tata_title=models.CharField(max_length=200)
    tata_price=models.CharField(max_length=100)
class TrackHistory(models.Model):
    url=models.URLField(max_length=300)
    user_price=models.IntegerField()
    user_email=models.EmailField()
    website=models.TextField(max_length=50)
    status=models.TextField(max_length=50)