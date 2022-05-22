from django.contrib import admin
from .models import Trade, CommodityPrice

# Register your models here.
admin.site.register(Trade)
admin.site.register(CommodityPrice)
