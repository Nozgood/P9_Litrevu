# Generated by Django 4.2.5 on 2023-10-06 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('litrevu_management', '0004_remove_ticket_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
