from django.contrib import admin
import price_scrap
from price_scrap.models import searchHistory
from price_scrap.models import TrackHistory
# Register your models here.
@admin.register(searchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['id','search_term','date_time','flipkart_title','flipkart_price','amazon_title','amazon_price','croma_title','croma_price','gadget_title','gadget_price','tata_title','tata_price']
@admin.register(TrackHistory)
class TrackHistoryAdmin(admin.ModelAdmin):
    list_display=['id','url','user_price','user_email','website','status']