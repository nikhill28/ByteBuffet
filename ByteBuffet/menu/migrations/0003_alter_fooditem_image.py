# Generated by Django 4.2.7 on 2024-01-04 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_fooditem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(upload_to='foodimages'),
        ),
    ]
