# Generated by Django 3.1.4 on 2021-09-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute_app', '0003_feedetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentdetails',
            name='s_pic',
            field=models.ImageField(db_column='s_pic', default=0, upload_to='Student/'),
            preserve_default=False,
        ),
    ]
