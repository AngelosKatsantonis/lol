# Generated by Django 3.1.1 on 2020-11-24 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game_assets', '0001_initial'),
        ('summoners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='series',
            field=models.ManyToManyField(to='summoners.Serie'),
        ),
        migrations.AddField(
            model_name='league',
            name='summoners',
            field=models.ManyToManyField(to='summoners.LeagueInfo'),
        ),
        migrations.AddField(
            model_name='item',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_assets.version'),
        ),
        migrations.AddField(
            model_name='champion',
            name='spells',
            field=models.ManyToManyField(to='game_assets.Spell'),
        ),
        migrations.AddField(
            model_name='champion',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game_assets.version'),
        ),
    ]
