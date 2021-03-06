# Generated by Django 2.1.4 on 2020-05-15 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0010_auto_20200512_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_goods_num', models.IntegerField(default=1)),
                ('c_is_select', models.BooleanField(default=True)),
                ('c_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Goods')),
            ],
            options={
                'db_table': 'axf_cart',
            },
        ),
        migrations.AlterField(
            model_name='axfuser',
            name='u_icon',
            field=models.ImageField(upload_to='icons/%y/%m/%d'),
        ),
        migrations.AddField(
            model_name='cart',
            name='c_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.AXFUser'),
        ),
    ]
