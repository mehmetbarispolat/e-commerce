# Generated by Django 4.2 on 2024-02-15 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("e_commerce", "0007_productstock_alter_product_stock_count"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="productstock",
            table="stock",
        ),
    ]