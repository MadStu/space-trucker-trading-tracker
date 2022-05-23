from django.contrib import admin
from .models import Trade, CommodityPrice, ErrorList

# Register your models here.
admin.site.register(Trade)
admin.site.register(CommodityPrice)
admin.site.register(ErrorList)
