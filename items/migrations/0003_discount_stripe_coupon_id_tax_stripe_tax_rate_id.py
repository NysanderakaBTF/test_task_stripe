# Generated by Django 5.1.6 on 2025-02-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_discount_tax_alter_item_price_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='stripe_coupon_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tax',
            name='stripe_tax_rate_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
