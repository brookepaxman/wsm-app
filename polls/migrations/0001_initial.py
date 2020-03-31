# Generated by Django 2.2.5 on 2020-03-26 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dummy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('hr', models.IntegerField(default=0)),
                ('rr', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField(verbose_name='date published')),
                ('startTime', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('sleepQuality', models.IntegerField(default=0)),
                ('sleepDisruptions', models.TextField()),
                ('sleepNotes', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.User')),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=0)),
                ('hr', models.IntegerField(default=0)),
                ('rr', models.IntegerField(default=0)),
                ('sessionID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Session')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.User')),
            ],
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date published')),
                ('tst', models.TimeField()),
                ('avgHR', models.IntegerField(default=0)),
                ('avgRR', models.IntegerField(default=0)),
                ('avgHRdip', models.IntegerField(default=0)),
                ('minHR', models.IntegerField(default=0)),
                ('maxHR', models.IntegerField(default=0)),
                ('minRR', models.IntegerField(default=0)),
                ('maxRR', models.IntegerField(default=0)),
                ('numSleepDisruptions', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.User')),
            ],
        ),
    ]
