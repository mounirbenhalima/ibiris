# Generated by Django 4.0.4 on 2022-05-24 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Marque')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Marque',
                'verbose_name_plural': 'Marques',
                'db_table': 'Brand',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Couleur')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Couleur',
                'verbose_name_plural': 'Couleurs',
                'db_table': 'Color',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Flavor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Parfum')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Parfum',
                'verbose_name_plural': 'Parfums',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Gamme',
                'verbose_name_plural': 'Gammes',
                'db_table': 'Range',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
                ('ref', models.CharField(blank=True, max_length=200, null=True)),
                ('product_designation', models.CharField(blank=True, max_length=200, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=1, default=0, max_digits=5, null=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Quantité')),
                ('threshold', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Seuil')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Prix')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.brand', verbose_name='Marque')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.color', verbose_name='Couleur')),
                ('flavor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.flavor', verbose_name='Parfum')),
                ('name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Product.range')),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
                'db_table': 'Product',
                'ordering': ['name__name', 'brand__name'],
            },
        ),
    ]
