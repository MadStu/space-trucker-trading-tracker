from django.contrib import admin
from .models import Trade, CommodityPrice, ErrorList, UserProfit, ShipList

admin.site.register(Trade)
admin.site.register(CommodityPrice)
admin.site.register(ErrorList)
admin.site.register(UserProfit)
admin.site.register(ShipList)
