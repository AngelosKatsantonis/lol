import time

from django.db import models

from django.conf import settings


class Region(models.Model):
    class meta:
        ordering = ['region']
    name = models.CharField(
                        unique=True,
                        max_length=255,
                        choices=settings.REGIONS
                    )


class SummonerHistory(models.Model):
    class Meta:
        ordering = ['summoner', '-timestamp']

    game_id = models.CharField(max_length=255)
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE)
    queue = models.CharField(max_length=50, choices=settings.QUEUES,
                             blank=False, default='')
    champion = models.PositiveIntegerField(default=0)
    timestamp = models.PositiveBigIntegerField(default=0)
    role = models.CharField(max_length=50, default='')
    lane = models.CharField(max_length=50, default='')

    def human_time(self):
        return time.ctime(self.timestamp/1000)


class Summoner(models.Model):
    class Meta:
        ordering = ['name']

    summoner_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    puuid = models.CharField(max_length=255, blank=True)
    account_id = models.CharField(max_length=255, blank=True)
    icon = models.PositiveIntegerField(default=0, blank=True)
    revision = models.PositiveBigIntegerField(default=0, blank=True)
    level = models.PositiveBigIntegerField(default=0, blank=True)


class SummonerSeries(models.Model):
    pass


class SummonerLeague(models.Model):
    class Meta:
        ordering = ['queue', 'tier', 'division', '-league_points']

    league_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE)
    queue = models.CharField(max_length=50, choices=settings.QUEUES,
                             blank=False, default='')
    tier = models.CharField(max_length=50, choices=settings.TIERS,
                            blank=False, default='')
    division = models.CharField(
            max_length=50, choices=settings.DIVISIONS, blank=False, default='')
    league_points = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    veteran = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    fresh_blood = models.BooleanField(default=False)
    hot_streak = models.BooleanField(default=False)

    def winrate(self):
        return round(self.wins/(self.wins + self.losses) * 100, 2)

    def tier_v(self):
        return dict(settings.TIERS)[self.tier]
