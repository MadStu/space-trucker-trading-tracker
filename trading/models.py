from django.db import models


class Trades(models.Model):
    commodity = models.CharField(max_length=50, null=False, blank=False)
    price = models.FloatField()
    amount = models.IntegerField()
    buy = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return self.commodity
