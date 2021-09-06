# Generated by Django 3.2.7 on 2021-09-04 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='FullReduce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_price', models.FloatField()),
                ('t_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_way', models.IntegerField(choices=[(1, 'Discount'), (2, 'Fullreduce'), (0, 'Null')], default=0)),
                ('discount_per', models.FloatField()),
                ('full_reduce_range', models.ManyToManyField(to='goods.FullReduce')),
            ],
        ),
        migrations.CreateModel(
            name='Coffe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coffe_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('price', models.FloatField(default=0)),
                ('vote', models.IntegerField(default=0)),
                ('discount', models.FloatField()),
                ('abstract_money', models.IntegerField(default=0)),
                ('pay_with_abstract_money', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.category')),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.attachment')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.promotion')),
            ],
        ),
    ]