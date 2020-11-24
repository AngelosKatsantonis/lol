from django.db import models

from django.conf import settings

from summoners.models import Summoner


class Team(models.Model):
    summoners = models.ManyToManyField(Summoner)
    side = models.CharField(max_length=10, choices=settings.TEAMS)
    win = models.BooleanField(blank=True)
    baronkills = models.PositiveIntegerField(default=0)
    dragonkills = models.PositiveIntegerField(default=0)
    towerkills = models.PositiveIntegerField(default=0)
    inhibitorkills = models.PositiveIntegerField(default=0)
    riftheraldkills = models.PositiveIntegerField(default=0)
    # bans = models.ManyToManyField(Champion) to be implemented


class Match(models.Model):
    game_id = models.CharField(max_length=255, unique=True)
    queue = models.CharField(max_length=50, choices=settings.QUEUES,
                             blank=False, default='')
    timestamp = models.PositiveBigIntegerField(default=0)
    duration = models.PositiveBigIntegerField(default=0)
    teams = models.ManyToManyField(Team)
