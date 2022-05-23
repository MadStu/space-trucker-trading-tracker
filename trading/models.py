from django.db import models


class Trade(models.Model):

    # Set Database fields
    commodity = models.CharField(max_length=150, null=False, blank=False)
    price = models.FloatField()
    amount = models.IntegerField()
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.commodity


class CommodityPrice(models.Model):
    # Set CommodityPrices Database fields
    code = models.CharField(max_length=4, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    kind = models.CharField(max_length=150, null=False, blank=False)
    trade_price_buy = models.FloatField()
    trade_price_sell = models.FloatField()
    date_modified = models.IntegerField()
    profit = models.FloatField()

    def __str__(self):
        return self.name
