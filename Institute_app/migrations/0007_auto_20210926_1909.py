# Generated by Django 3.1.4 on 2021-09-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute_app', '0006_auto_20210926_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedetails',
            name='status',
            field=models.CharField(db_column='status', default='not paid', max_length=20),
        ),
    ]
