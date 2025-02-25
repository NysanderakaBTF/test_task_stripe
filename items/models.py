from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)  # Цена в валюте с сотыми
    currency = models.CharField(max_length=3, default='usd')  # Валюта (usd, eur и т.д.)

    def __str__(self):
        return self.name

class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # в процентах
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True)  # ID купона в Stripe
    
    def __str__(self):
        return self.name + ' - ' + str(self.amount)


class Order(models.Model):
    items = models.ManyToManyField(Item)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    discounts = models.ManyToManyField(Discount, blank=True)
    @property
    def total_price(self):
        total_price_wo_discount = self.items.aggregate(models.Sum("price")).get("price__sum", 0)
        if self.discounts.exists():
            discount = self.discounts.all().aggregate(models.Sum("amount")).get("amount__sum", 0)
            if discount > 100:
                discount = 100
        else:
            discount = 0
        return total_price_wo_discount*(100-discount)/100

    def get_currency(self):
        return self.items.first().currency if self.items.exists() else 'usd'