# Generated by Django 2.1.4 on 2020-05-18 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20200515_1742'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_time', models.DateTimeField(auto_now=True)),
                ('o_status', models.IntegerField(verbose_name=1)),
                ('o_price', models.FloatField(default=0)),
                ('o_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.AXFUser')),
            ],
            options={
                'db_table': 'axf_order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_goods_num', models.IntegerField(default=1)),
                ('o_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Goods')),
                ('o_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Order')),
            ],
            options={
                'db_table': 'axf_ordergoods',
            },
        ),
    ]
