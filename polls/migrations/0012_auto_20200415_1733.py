# Generated by Django 2.2.5 on 2020-04-15 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20200415_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='sleepQuality',
            field=models.IntegerField(default=0),
        ),
    ]