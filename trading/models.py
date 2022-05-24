from django.db import models


class Trade(models.Model):
    commodity = models.CharField(max_length=150, null=False, blank=False)
    price = models.FloatField()
    amount = models.IntegerField()
    cost = models.FloatField(default=0)
    value = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    session = models.CharField(max_length=150, blank=False, default=0)
    time = models.IntegerField(default=0)
    buy = models.BooleanField(default=True)
    units = models.IntegerField(default=5000)

    def __str__(self):
        return self.commodity


class CommodityPrice(models.Model):
    code = models.CharField(max_length=4, null=False, blank=False)
    name = models.CharField(max_length=150, null=False, blank=False)
    kind = models.CharField(max_length=150, null=False, blank=False)
    trade_price_buy = models.FloatField()
    trade_price_sell = models.FloatField()
    date_modified = models.IntegerField()
    profit = models.FloatField()

    def __str__(self):
        return self.name


class ErrorList(models.Model):
    error_message = models.CharField(max_length=150, null=False, blank=False)
    error_location = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self):
        return self.error_message
