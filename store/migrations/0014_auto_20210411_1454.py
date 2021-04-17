# Generated by Django 3.1.7 on 2021-04-11 12:54

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210410_0151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='telephone',
            field=models.CharField(max_length=8, null=True, validators=[store.models.is_number]),
        ),
    ]