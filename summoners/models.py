import time

from django.db import models

from django.conf import settings

from game_assets.models import SummonerIcon, Champion


class Summoner(models.Model):
    class Meta:
        ordering = ['name']

    summoner_id = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    region = models.ForeignKey('game_assets.Region', on_delete=models.CASCADE)
    puuid = models.CharField(max_length=255, blank=True)
    account_id = models.CharField(max_length=255)
    icon = models.CharField(max_length=10,  blank=True)
    revision = models.PositiveBigIntegerField(default=0, blank=True)
    level = models.PositiveBigIntegerField(default=0, blank=True)

    def get_icon(self):
        icon = SummonerIcon.objects.filter(key=self.icon)
        if icon.exists():
            return icon
        else:
            return None


class History(models.Model):
    class Meta:
        ordering = ['summoner']

    summoner = models.ForeignKey('Summoner', on_delete=models.PROTECT)
    champion = models.CharField(max_length=10, default='')
    role = models.CharField(max_length=50, default='')
    lane = models.CharField(max_length=50, default='')
    spells = models.CharField(max_length=50, default='')
    kills = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    deaths = models.PositiveIntegerField(default=0)
    cs = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    doublekills = models.PositiveIntegerField(default=0)
    triplekills = models.PositiveIntegerField(default=0)
    quadrakills = models.PositiveIntegerField(default=0)
    pentakills = models.PositiveIntegerField(default=0)
    unrealkills = models.PositiveIntegerField(default=0)
    items = models.CharField(max_length=50, default='')
    skill_order = models.CharField(max_length=50, default='')

    def get_champion(self):
        champion = Champion.objects.filter(key=self.champion)
        if champion.exists():
            return champion
        else:
            return None


class Team(models.Model):
    team_choices = [
        (100, 'Blue'),
        (200, 'Red'),
    ]
    summoners = models.ManyToManyField(History)
    side = models.PositiveIntegerField(choices=team_choices, default=100)
    win = models.BooleanField(default=False)
    barons = models.PositiveIntegerField(default=0)
    towers = models.PositiveIntegerField(default=0)
    inhibitors = models.PositiveIntegerField(default=0)
    dragons = models.PositiveIntegerField(default=0)
    riftheralds = models.PositiveIntegerField(default=0)
    bans = models.CharField(max_length=100)


class Match(models.Model):
    game_id = models.CharField(max_length=255)
    timestamp = models.PositiveBigIntegerField(default=0)
    duration = models.PositiveBigIntegerField(default=0)
    queue = models.CharField(max_length=50, choices=settings.QUEUES,
                             blank=False, default='')
    teams = models.ManyToManyField(Team)

    def human_time(self):
        return time.ctime(self.timestamp/1000)


class Serie(models.Model):
    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE)
    target = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    progress = models.CharField(max_length=10, default='')


class LeagueInfo(models.Model):
    class Meta:
        ordering = ['-league_points', 'wins']

    summoner = models.ForeignKey('Summoner', on_delete=models.CASCADE)
    league_points = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    veteran = models.BooleanField(default=False)
    inactive = models.BooleanField(default=False)
    fresh_blood = models.BooleanField(default=False)
    hot_streak = models.BooleanField(default=False)

    def winrate(self):
        return round(self.wins/(self.wins + self.losses) * 100, 2)
