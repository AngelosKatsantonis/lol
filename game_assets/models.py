from django.db import models

from django.conf import settings


class Region(models.Model):
    class meta:
        ordering = ['name']
    name = models.CharField(
                        unique=True,
                        max_length=10,
                        choices=settings.REGIONS)


class Version(models.Model):

    class meta:
        ordering = ['game_version']

    game_version = models.CharField(max_length=10, default='', unique=True)
    regions = models.ManyToManyField(Region)


class SummonerIcon(models.Model):
    key = models.CharField(max_length=10)
    icon = models.ImageField(upload_to='summonericons/')
    version = models.ForeignKey(Version, on_delete=models.CASCADE)


class League(models.Model):

    class Meta:
        ordering = ['queue', 'tier', 'division']

    summoners = models.ManyToManyField('summoners.LeagueInfo')
    queue = models.CharField(max_length=50, choices=settings.QUEUES,
                             blank=False, default='')
    tier = models.CharField(max_length=50, choices=settings.TIERS,
                            blank=False, default='')
    division = models.CharField(max_length=50, choices=settings.DIVISIONS)
    icon = models.ImageField(upload_to='leagueicons/')
    series = models.ManyToManyField('summoners.Serie')


class Position(models.Model):
    name = models.CharField(max_length=10,
                            choices=settings.SUMMONER_POSITIONS)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='positionicons/')


class Spell(models.Model):
    class meta:
        ordering = ['key']

    name = models.CharField(max_length=50)
    key = models.CharField(max_length=10, blank=True)
    icon = models.ImageField(upload_to='spellicons/')
    keybind = models.CharField(max_length=2)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    cost = models.CharField(max_length=100, blank=True)
    cooldown = models.CharField(max_length=100, blank=True)
    spell_range = models.CharField(max_length=100, blank=True)


class Item(models.Model):
    class meta:
        ordering = ['key']

    name = models.CharField(max_length=50)
    key = models.CharField(max_length=10)
    icon = models.ImageField(upload_to='itemicons/')
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    cost = models.PositiveIntegerField(default=0)
    sell = models.PositiveIntegerField(default=0)


class Champion(models.Model):

    class meta:
        ordering = ['name']

    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    key = models.CharField(max_length=10)
    icon = models.ImageField(upload_to='championicons/')
    spells = models.ManyToManyField(Spell)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)

    def get_actives(self):
        return self.spells.exclude(keybind='p').all()

    def get_passive(self):
        return self.spells.filter(keybind='p').get()
