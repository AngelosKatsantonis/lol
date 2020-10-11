# Generated by Django 3.1.1 on 2020-10-11 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summoners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SummonerSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='version',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(choices=[('eun1', 'Europe Nordic & East'), ('euw1', 'Europe West')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='summonerhistory',
            name='queue',
            field=models.CharField(choices=[('RANKED_SOLO_5x5', '5v5 Ranked Solo games')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='summonerleague',
            name='queue',
            field=models.CharField(choices=[('RANKED_SOLO_5x5', '5v5 Ranked Solo games')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='summonerleague',
            name='tier',
            field=models.CharField(choices=[('CHALLENGER', 'Challenger'), ('DIAMOND', 'Diamond')], default='', max_length=50),
        ),
    ]
