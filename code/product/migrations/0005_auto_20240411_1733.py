# Generated by Django 2.2.1 on 2024-04-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20230716_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='Product',
            new_name='product',
        ),
    ]
