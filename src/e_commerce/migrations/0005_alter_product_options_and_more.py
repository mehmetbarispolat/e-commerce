# Generated by Django 4.2 on 2024-02-14 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("e_commerce", "0004_alter_product_description_alter_product_price_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["-created_at"]},
        ),
        migrations.RenameField(
            model_name="product",
            old_name="created_on",
            new_name="created_at",
        ),
    ]
