# Generated by Django 4.2.7 on 2023-11-19 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], max_length=20, null=True),
        ),
    ]
