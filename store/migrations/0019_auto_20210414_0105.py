# Generated by Django 3.1.7 on 2021-04-13 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20210413_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(limit_choices_to={'parent__isnull': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='store.categorie'),
        ),
    ]
