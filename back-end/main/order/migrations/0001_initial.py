# Generated by Django 5.1 on 2024-09-27 23:11

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0001_initial'),
        ('material', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.CharField(max_length=2000, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(2000)])),
                ('hourly_rate', models.FloatField(default=93.0, validators=[django.core.validators.MinValueValidator(75.0)])),
                ('hours_worked', models.FloatField(default=3.0, validators=[django.core.validators.MinValueValidator(3.0)])),
                ('material_upcharge', models.FloatField(default=25.0, validators=[django.core.validators.MinValueValidator(15.0), django.core.validators.MaxValueValidator(75.0)])),
                ('tax', models.FloatField(default=12.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(20.0)])),
                ('total', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('completed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('discount', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('notes', models.CharField(blank=True, max_length=10000, null=True, validators=[django.core.validators.MaxLengthValidator(10000)])),
                ('callout', models.FloatField(choices=[('50.0', 'Standard - $50.00'), ('175.0', 'Emergency - $175.00')], default='50.0')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
        migrations.CreateModel(
            name='OrderCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, validators=[django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(300)])),
                ('cost', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costs', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.material')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('cash', 'Cash'), ('check', 'Check')], max_length=5)),
                ('total', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('notes', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='orders')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='order.order')),
            ],
        ),
    ]
