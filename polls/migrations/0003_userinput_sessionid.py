# Generated by Django 2.2.5 on 2020-03-26 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_analysis_sessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinput',
            name='sessionID',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.Session'),
            preserve_default=False,
        ),
    ]
