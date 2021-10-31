# Generated by Django 3.1.4 on 2021-09-26 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Institute_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_address',
            field=models.CharField(db_column='tr_add', max_length=200),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_dob',
            field=models.CharField(db_column='tr_dob', max_length=20),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_email',
            field=models.CharField(db_column='tr_email', max_length=50),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_gender',
            field=models.CharField(db_column='tr_gender', max_length=10),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_id',
            field=models.IntegerField(db_column='tr_id', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_join',
            field=models.CharField(db_column='tr_join', max_length=10),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_name',
            field=models.CharField(db_column='tr_name', max_length=30),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_passwd',
            field=models.CharField(db_column='tr_passwd', max_length=20),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_phno',
            field=models.CharField(db_column='tr_phno', max_length=10),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_pic',
            field=models.ImageField(db_column='tr_pic', upload_to='HR/'),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_qual',
            field=models.CharField(db_column='tr_qual', default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='trainerdetails',
            name='tr_status',
            field=models.CharField(db_column='tr_status', default='active', max_length=30),
        ),
    ]
