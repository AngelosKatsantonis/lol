import requests
import logging
import uuid
import os

from PIL import Image

from django.conf import settings

from game_assets.models import (Version, Champion, Spell, Item,
                                SummonerIcon, Region, League, Position)


# Globals for syncing game_assets
global logger
global game_regions
global versions
global versions_url
global all_champions_url
global champion_url
global champion_square_url
global champion_spell_url
global champion_passive_url
global spell_keybinds
global summoner_spells_url
global summoner_spell_url
global items_url
global item_url
global summoner_icons_url
global summoner_icon_url
global base_dir
global media_root
global tiers
global master_tiers
global queues
global divisions
global positions

logger = logging.getLogger(__name__)
game_regions = settings.REGIONS
versions = settings.VERSIONS
versions_url = settings.VERSIONS_URL
all_champions_url = settings.ALL_CHAMPIONS_URL
champion_url = settings.CHAMPION_URL
champion_square_url = settings.CHAMPION_SQUARE_URL
champion_spell_url = settings.CHAMPION_SPELL_URL
champion_passive_url = settings.CHAMPION_PASSIVE_URL
spell_keybinds = settings.SPELL_KEYBINDS
summoner_spells_url = settings.SUMMONER_SPELLS_URL
summoner_spell_url = settings.SUMMONER_SPELL_URL
items_url = settings.ITEMS_URL
item_url = settings.ITEM_URL
summoner_icons_url = settings.SUMMONER_ICONS_URL
summoner_icon_url = settings.SUMMONER_ICON_URL
base_dir = str(settings.BASE_DIR)
media_root = settings.MEDIA_ROOT
tiers = settings.TIERS
master_tiers = settings.MASTER_TIERS
queues = settings.QUEUES
divisions = settings.DIVISIONS
positions = settings.SUMMONER_POSITIONS


def spell_list_to_str(attr=[]):
    if len(set(attr)) == 1:
        return str(attr[0])
    else:
        return '/'.join([str(x) for x in attr])


def ensure_paths(paths=[]):
    for path in paths:
        full_path = base_dir + media_root + path
        if not os.path.exists(full_path):
            os.makedirs(full_path)
    logger.warning('Paths present')


def get_icon(url='', fp='', version=''):
    v = 'v' + version.replace('.', '') + '_'
    response = requests.get(url, stream=True)
    img = Image.open(response.raw)
    fn = uuid.uuid4().hex
    filepath = fp + v + fn + '.png'
    img.save(base_dir + media_root + filepath)
    return filepath


def create_regions(data=None):
    regions = [Region.objects.get_or_create(name=each[0]) for each in data]
    created = [region[0] for region in regions if region[1]]
    if len(created) > 0:
        logger.warning('Created regions %s' % ','.join(
                                            [r.name for r in created]))
    logger.warning('Regions synced')
    return created


def create_versions(regions=[]):
    for region in regions:
        url = versions_url + versions[region.name] + '.json'
        response = requests.get(url)
        version = response.json()['v']
        new_version, created = Version.objects.get_or_create(
                                                game_version=version)
        if created:
            logger.warning('Created version %s' % new_version.game_version)
        if region in new_version.regions.all():
            continue
        else:
            new_version.regions.add(region)
            old_versions = Version.objects.exclude(
                            game_version=version).filter(regions=region)
            [version.regions.remove(region) for version in old_versions]
    logger.warning('Versions synced')
    return Version.objects.all()


def create_champions(version=None):
    url = all_champions_url.format(version=version.game_version)
    response = requests.get(url)
    data = response.json()['data']
    champions = [each for each in data.keys()]
    for each in champions:
        url = champion_url.format(version=version.game_version,
                                  champion=each)
        response = requests.get(url)
        data = response.json()['data']
        if data is not None:
            champion = Champion.objects.filter(version=version,
                                               name=data[each]['name'])
            if champion.exists():
                continue
            champion = {}
            champion['version'] = version
            champion['name'] = data[each]['name']
            champion['title'] = data[each]['title']
            champion['key'] = data[each]['key']
            url = champion_square_url.format(
                version=version.game_version,
                full=data[each]['image']['full'])
            champion['icon'] = get_icon(url=url, fp='championicons/',
                                        version=version.game_version)
            champion = Champion.objects.create(**champion)
            passive = {}
            passive['version'] = version
            passive['name'] = data[each]['passive']['name']
            passive['keybind'] = 'p'
            url = champion_passive_url.format(
                    version=version.game_version,
                    full=data[each]['passive']['image']['full'])

            passive['icon'] = get_icon(url=url, fp='spellicons/',
                                       version=version.game_version)
            passive = Spell.objects.create(**passive)
            champion.spells.add(passive)
            spells = data[each]['spells']
            for spell in range(len(spells)):
                new_spell = {}
                new_spell['version'] = version
                new_spell['name'] = spells[spell]['name']
                new_spell['description'] = spells[spell]['description']
                new_spell['keybind'] = spell_keybinds[spell]
                url = champion_spell_url.format(
                    version=version.game_version,
                    full=spells[spell]['image']['full'])
                new_spell['icon'] = get_icon(url=url, fp='spellicons/',
                                             version=version.game_version)
                new_spell['cooldown'] = spell_list_to_str(
                                                spells[spell]['cooldown'])
                new_spell['cost'] = spell_list_to_str(spells[spell]['cost'])
                new_spell['spell_range'] = spell_list_to_str(
                                                spells[spell]['range'])
                new_spell = Spell.objects.create(**new_spell)
                champion.spells.add(new_spell)

            logger.info('Created champion %s for version %s' % (each,
                                                        version.game_version))
    logger.warning('Champions synced')


def create_spells(version=None):
    url = summoner_spells_url.format(version=version.game_version)
    response = requests.get(url)
    data = response.json()['data']
    for key, spell in data.items():
        old_spell = Spell.objects.filter(version=version, name=spell['name'])
        if old_spell.exists():
            continue
        new_spell = {}
        new_spell['version'] = version
        new_spell['name'] = spell['name']
        new_spell['description'] = spell['description']
        new_spell['keybind'] = 'df'
        new_spell['key'] = spell['key']
        url = summoner_spell_url.format(
                        version=version.game_version,
                        full=spell['image']['full'])
        new_spell['icon'] = get_icon(url=url, fp='spellicons/',
                                     version=version.game_version)
        Spell.objects.create(**new_spell)
        logger.info('Created spell %s for version %s' % (key,
                                                         version.game_version))
    logger.warning('Summoner spells synced')


def create_summoner_icons(version=None):
    url = summoner_icons_url.format(version=version.game_version)
    response = requests.get(url)
    data = response.json()['data']
    for key, icon in data.items():
        old_icon = SummonerIcon.objects.filter(version=version, key=key)
        if old_icon.exists() or key == 'placeholder':
            continue
        new_icon = {}
        new_icon['version'] = version
        new_icon['key'] = key
        url = summoner_icon_url.format(
                        version=version.game_version,
                        full=icon['image']['full'])
        new_icon['icon'] = get_icon(url=url, fp='summonericons/',
                                    version=version.game_version)
        SummonerIcon.objects.create(**new_icon)
        logger.info('Created summoner icon %s for version %s' % (key,
                                                version.game_version))
    logger.warning('Summoner icons synced')


def create_items(version=None):
    url = items_url.format(version=version.game_version)
    response = requests.get(url)
    data = response.json()['data']
    for key, item in data.items():
        old_item = Item.objects.filter(version=version, key=key)
        if old_item.exists():
            continue
        new_item = {}
        new_item['version'] = version
        new_item['description'] = item['description']
        new_item['cost'] = item['gold']['total']
        new_item['sell'] = item['gold']['sell']
        new_item['name'] = item['name']
        new_item['key'] = key
        url = item_url.format(
                        version=version.game_version,
                        full=item['image']['full'])
        new_item['icon'] = get_icon(url=url, fp='itemicons/',
                                    version=version.game_version)
        Item.objects.create(**new_item)
        logger.info('Created item %s for version %s' % (key,
                                                        version.game_version))

    logger.warning('Items synced')


def delete_obsolete_versions(paths=[]):
    obsolete_versions = Version.objects.filter(regions=None)
    versions = [v.game_version for v in obsolete_versions]
    if len(obsolete_versions) > 0:
        for version in versions:
            v = 'v' + version.replace('.', '') + '_'
            for path in paths:
                fp = base_dir + media_root + path
                for f in os.listdir(fp):
                    if f.startswith(v):
                        os.remove(os.path.join(fp, f))
        logger.warning('Obsolete versions %s deleted' % ','.join(versions))
        [version.delete() for version in obsolete_versions]
    logger.warning('No obsolete versions left in the data')


def create_leagues():
    fp = base_dir + media_root + 'leagueicons/'
    for queue in queues:
        for tier in tiers:
            for division in divisions:
                new = {}
                new['queue'] = queue[0]
                new['tier'] = tier[0]
                new['division'] = division[0]
                new['icon'] = fp + '%s.png' % tier[0]
                league, created = League.objects.get_or_create(**new)
                if created:
                    logger.info('Created league %s %s for queue %s' % (
                                        tier[0], division[0], queue[0]))
                    create_positions(league=league)
        for tier in master_tiers:
            new = {}
            new['queue'] = queue[0]
            new['tier'] = tier[0]
            new['division'] = 'I'
            new['icon'] = fp + '%s.png' % tier[0]
            league, created = League.objects.get_or_create(**new)
            if created:
                logger.info('Created league %s for queue %s' % (
                                    tier[0], queue[0]))
                create_positions(league=league)
            pass
    logger.warning('Leagues synced')


def create_positions(league=None):
    fp = base_dir + media_root + 'positionicons/'
    for position in positions:
        new = {}
        new['name'] = position[0]
        new['league'] = league
        new['icon'] = fp + '%s_%s.png' % (league.tier, position[0])
        Position.objects.create(**new)
        if league.division is None:
            logger.info('Created position %s for league %s' % (position[0],
                                                               league.tier))
        else:
            logger.info('Created position %s for league %s %s' % (position[0],
                                                league.tier, league.division))

def sync_game_assets():
    iconpaths = [
        'itemicons/',
        'summonericons/',
        'championicons/',
        'spellicons/',
    ]
    logger.warning('Syncing game assets')
    ensure_paths(iconpaths)
    create_leagues()
    regions = create_regions(game_regions)
    versions = create_versions(regions)
    for version in versions:
        logger.warning('Syncing champions')
        create_champions(version)
        logger.warning('Syncing summoner spells')
        create_spells(version)
        logger.warning('Syncing items')
        create_items(version)
        logger.warning('Syncing summoner icons')
        create_summoner_icons(version)
    delete_obsolete_versions(iconpaths)
    logger.warning('Syncing game assets finished')
