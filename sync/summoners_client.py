import requests
import logging
import time
import threading

from django.conf import settings

from game_assets.models import Region, League
from summoners.models import Summoner, LeagueInfo, History, Serie, Match, Team

global logger
global conversions
global headers
global queues
global tiers
global master_tiers
global divisions
global endpoints
global riot_api_url
global qcodes
global qcodes_reverse
global max_requests
global minutes
global spell_keybinds

logger = logging.getLogger(__name__)
headers = {'X-Riot-Token': settings.RIOT_TOKEN}
qcodes = settings.QCODES
qcodes_reverse = settings.QCODES_REVERSE
conversions = settings.CONVERSIONS
queues = settings.QUEUES
#tiers = settings.TIERS
#master_tiers = settings.MASTER_TIERS
#divisions = settings.DIVISIONS
endpoints = settings.RIOT_ENDPOINTS
riot_api_url = settings.RIOT_API_URL
spell_keybinds = settings.SPELL_KEYBINDS
max_requests = 100
minutes = 2

master_tiers = []
tiers = [('GOLD', 'Gold')]
divisions = [('II', 'II')]


def get_summoner_by_name(name='', region_name=''):
    logger.info('Request data for summoner %s in region %s' % (name,
                                                               region_name))
    start = time.time()
    count = 2
    timeout = 0
    data = requests_get(region_name=region_name, param=name,
                        endpoint=endpoints['summoner_by_name'])
    region = Region.objects.filter(name=region_name)
    if region.exists() and data is not None:
        region = region.get()
        clean_data = {(conversions[k] if k in conversions.keys() else k
                       ): v for k, v in data.items()}
        clean_data['region'] = region
        summoner = create_summoner(data=clean_data)
        league_data = requests_get(region_name=region.name,
                                   param=summoner.summoner_id,
                                   endpoint=endpoints['league'])
        temp = [{(conversions[k] if k in conversions.keys() else k
                  ): v for k, v in each.items()} for each in league_data]
        leagues_info = [{k: v for k, v in each.items(
                                ) if k not in (
                'league_id', 'summoner_id', 'name')} for each in temp]
        for league_info in leagues_info:
            league_info['summoner'] = summoner
            league = {
                'queue': league_info.pop('queue'),
                'tier': league_info.pop('tier'),
                'division': league_info.pop('division'),
            }
            if 'mini_series' in league_info.keys():
                series = league_info.pop('mini_series')
                series['summoner'] = summoner
                create_series(data=series, league=league)
            create_league_info(data=league_info, league=league)
        for queue in queues:
            tts_data = {
                'start': start,
                'count': count,
                'timeout': timeout
            }
            start, count, timeout = update_summoner_history(
                                    account_id=summoner.account_id,
                                    region=region,
                                    queue=queue[0],
                                    days=1,
                                    tts_data=tts_data)
        return summoner
    else:
        logger.warning('No data for summoner %s in region %s' % (
                                            name, region_name))
        return None


def get_summoner_by_league(league_data={}, region=None):
    summoner_id = league_data['summonerId']
    data = requests_get(region_name=region.name, param=summoner_id,
                        endpoint=endpoints['summoner_by_id'])
    if data is not None and league_data is not None:
        clean_data = {(conversions[k] if k in conversions.keys() else k
                       ): v for k, v in data.items()}
        clean_data['region'] = region
        summoner = create_summoner(data=clean_data)
        temp = {(conversions[k] if k in conversions.keys() else k
                 ): v for k, v in league_data.items()}
        league_info = {k: v for k, v in temp.items(
                                        ) if k not in (
                            'league_id', 'summoner_id', 'name')}
        league_info['summoner'] = summoner
        league = {
            'queue': league_info.pop('queue'),
            'tier': league_info.pop('tier'),
            'division': league_info.pop('division'),
        }
        if 'mini_series' in league_info.keys():
            series = league_info.pop('mini_series')
            series['summoner'] = summoner
            create_series(data=series, league=league)
        create_league_info(data=league_info, league=league)
        return summoner
    else:
        logger.warning('No data for summoner %s in region %s' % (
                                            summoner_id, region.name))
        return None


def create_series(data=None, league={}):
    new_league = League.objects.filter(queue=league['queue'],
                                       tier=league['tier'],
                                       division=league['division'])
    old_league = League.objects.filter(queue=league['queue'],
                                       series__summoner=data['summoner'])
    if old_league.exists():
        serie = old_league.get().series.filter(summoner=data['summoner'])
        serie.update(**data)
        new_league.get().series.add(serie.get())
        old_league.get().series.remove(serie.get())
        logger.info('Updated serie for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, league['queue']))
    else:
        info = Serie.objects.create(**data)
        new_league.get().series.add(info)
        logger.info('Created serie for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, league['queue']))


def process_frames(data=[]):
    skillups = {x: '' for x in range(1, 11)}
    for f in data:
        if len(f['events']) > 0:
            for e in f['events']:
                if e['type'] == 'SKILL_LEVEL_UP':
                    if e['skillSlot'] in (1, 2, 3, 4):
                        skillups[e['participantId']] += spell_keybinds[
                                                            e['skillSlot']-1
                                                            ]
    return skillups


def update_summoner_history(account_id='', region=None, queue='', days=1,
                            tts_data={}):
    if tts_data:
        start = tts_data['start']
        count = tts_data['count']
        timeout = tts_data['timeout']
        tts_Enabled = True
    else:
        start = 0
        count = 0
        timeout = 0
        tts_Enabled = False

    logger.info('Updating history for summoner %s and queue %s' % (
                                                account_id, queue))
    begin_time = int(time.time() - (86400*days))
    start, count, timeout = get_tts(start, count, timeout, 1)
    count += 1
    history_data = requests_get(region_name=region.name,
                                param=account_id,
                                endpoint=endpoints['summoner_history'],
                                params={
                                    'beginTime': begin_time,
                                    'endIndex': 100,
                                    'queue': qcodes[queue],
                                })
    if history_data is not None:
        game_ids = [m['gameId'] for m in history_data['matches']]
    else:
        game_ids = []
        logger.info('No history for summoner %s and queue %s' % (account_id,
                                                                 queue))
    for game_id in game_ids:
        match = Match.objects.filter(game_id=game_id)
        if match.exists():
            logger.info('Match %s already exists' % game_id)
            continue
        start, count, timeout = get_tts(start, count, timeout, 2)
        count += 2
        match_data = requests_get(region_name=region.name,
                                  param=game_id,
                                  endpoint=endpoints['match'])
        timeline_data = requests_get(region_name=region.name,
                                     param=game_id,
                                     endpoint=endpoints['timeline'])
        if match_data is None or timeline_data is None:
            logger.warning('No data for match %s' % game_id)
            continue
        skillups = process_frames(timeline_data['frames'])
        match = {
            'game_id': game_id,
            'timestamp': match_data['gameCreation'],
            'duration': match_data['gameDuration'],
            'queue': qcodes_reverse[match_data['queueId']]
        }
        match = Match.objects.create(**match)
        logger.info('Created match %s' % game_id)
        teams = {}
        for t in match_data['teams']:
            team = {
                'side': t['teamId'],
                'win': (True if t['win'] == 'Win' else False),
                'barons': t['baronKills'],
                'towers': t['towerKills'],
                'inhibitors': t['inhibitorKills'],
                'dragons': t['dragonKills'],
                'riftheralds': t['riftHeraldKills'],
                'bans': '/'.join(
                        [str(ban['championId']) for ban in t['bans']])
            }
            team = Team.objects.create(**team)
            teams[t['teamId']] = team
            match.teams.add(team)
        summoners = {}
        for s in match_data['participantIdentities']:
            current_account_id = s['player']['currentAccountId']
            current_region = s['player']['currentPlatformId'].lower()
            summoner = Summoner.objects.filter(
                        account_id=current_account_id,
                        region__name=current_region)
            if summoner.exists():
                summoner = summoner.get()
            else:
                start, count, timeout = get_tts(start, count, timeout, 1)
                count += 1
                region = Region.objects.filter(
                        name=current_region).get()
                data = requests_get(
                        region_name=current_region,
                        param=current_account_id,
                        endpoint=endpoints['summoner_by_account'])
                if data is not None:
                    data = {(conversions[k] if k in conversions.keys(
                            ) else k): v for k, v in data.items()}
                else:
                    data = {
                        'account_id': current_account_id,
                    }
                data['region'] = region
                summoner = Summoner.objects.create(**data)
            summoners[s['participantId']] = summoner
        for p in match_data['participants']:
            h = {
                'summoner': summoners[p['participantId']],
                'spells': str(p['spell1Id']) + '/' + str(p['spell2Id']),
                'champion': str(p['championId']),
                'kills': p['stats']['deaths'],
                'deaths': p['stats']['kills'],
                'assists': p['stats']['assists'],
                'cs': p['stats']['totalMinionsKilled'],
                'gold': p['stats']['goldEarned'],
                'doublekills': p['stats']['doubleKills'],
                'triplekills': p['stats']['tripleKills'],
                'quadrakills': p['stats']['quadraKills'],
                'pentakills': p['stats']['pentaKills'],
                'unrealkills': p['stats']['unrealKills'],
                'items': (str(p['stats']['item0']) + '/' +
                          str(p['stats']['item1']) + '/' +
                          str(p['stats']['item2']) + '/' +
                          str(p['stats']['item3']) + '/' +
                          str(p['stats']['item4']) + '/' +
                          str(p['stats']['item5']) + '/' +
                          str(p['stats']['item6'])),
                'role': p['timeline']['role'],
                'lane': p['timeline']['lane'],
                'skill_order': skillups[p['participantId']]
            }
            teams[p['teamId']].summoners.add(History.objects.create(**h))
    logger.info('History updated for summoner %s' % account_id)
    if tts_Enabled:
        return start, count, timeout


def requests_get(region_name='', param='', endpoint='', params={}):
    url = 'https://%s.%s%s%s' % (
                                region_name,
                                riot_api_url,
                                endpoint,
                                param)
    logger.info('Request send to %s' % url)
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        logger.error('Response message: %s' % response.json(
                                        )['status']['message'])
        return None
    else:
        return response.json()


def convert_divisionless_league(data=None):
    if data is None:
        logger.error('Cannot convert because data %s' % str(data))
        return []
    common = {k: v for k, v in data.items() if k not in ('entries',)}
    league = [{**common, **each} for each in data['entries']]
    return league


def create_summoner(data=None):
    logger.info('Creating summoner %s in region %s' %
                (data['summoner_id'], data['region'].name))

    old_summoner = Summoner.objects.filter(puuid=data['puuid'],
                                           region=data['region'],)
    if old_summoner.exists():
        old_summoner.update(**data)
        summoner = old_summoner.get()
        logger.info('Updated summoner %s in region %s' %
                    (data['summoner_id'], data['region'].name))
    else:
        summoner = Summoner.objects.create(**data)
        logger.info('Created summoner %s in region %s' %
                    (data['summoner_id'], data['region'].name))
    return summoner


def create_league_info(data=None, league={}):
    new_league = League.objects.filter(queue=league['queue'],
                                       tier=league['tier'],
                                       division=league['division'])
    old_league = League.objects.filter(queue=league['queue'],
                                       summoners__summoner=data['summoner'])
    if old_league.exists():
        info = old_league.get().summoners.filter(summoner=data['summoner'])
        info.update(**data)
        new_league.get().summoners.add(info.get())
        old_league.get().summoners.remove(info.get())
        logger.info('Updated league info for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, league['queue']))
    else:
        info = LeagueInfo.objects.create(**data)
        new_league.get().summoners.add(info)
        logger.info('Created league info for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, league['queue']))


def delete_obsolete_summoners(summoners=[], region=None):
    all_summoners = Summoner.objects.filter(region=region)
    [s.delete() for s in all_summoners if s not in summoners]
    logger.warning('Deleted obsolete summoners on region %s' % region.name)


def get_tts(start=None, count=0, timeout=0, reqs=0):
    elapsed = time.time() - start
    if count + reqs > max_requests and elapsed <= 60*minutes:
        tts = round((60*minutes) - elapsed)
        timeout += tts
        logger.warning('Pausing sync for %s seconds' % str(tts))
        time.sleep(tts)
        count = 0
        start = time.time()
        logger.warning('Resuming sync')
    return start, count, timeout


def update_region(region=None, days=1):
    logger.warning('Syncing %s at %s' % (region.name, time.ctime(time.time())))
    sync_start = time.time()
    timeout = 0
    count = 0
    start = time.time()
    all_summoners = []
    for queue in queues:
        logger.warning('Syncing leagues %s %s' % (region.name, queue[0]))
        if queue[0] not in ('RANKED_FLEX_SR', 'RANKED_SOLO_5x5'):
            logger.warning('Skipping %s %s' % (region.name, queue[0]))
        else:
            leagues = []
            for tier in master_tiers:
                start, count, timeout = get_tts(start, count, timeout, 1)
                count += 1
                data = requests_get(region_name=region.name, param=queue[0],
                                    endpoint=endpoints[tier[0].lower()])
                converted = convert_divisionless_league(data)
                leagues += converted
            for tier in tiers:
                for division in divisions:
                    start, count, timeout = get_tts(start, count, timeout, 1)
                    count += 1
                    param = queue[0] + '/' + tier[0] + '/' + division[0]
                    data = requests_get(region_name=region.name, param=param,
                                        endpoint=endpoints['leagues'])
                    leagues += data
            summoners = []
            for each in leagues:
                start, count, timeout = get_tts(start, count, timeout, 1)
                count += 1
                summoners.append(get_summoner_by_league(each, region))
            logger.warning('Synced leagues %s %s' % (region.name, queue[0]))
            all_summoners += summoners
        for s in summoners:
            tts_data = {
                'start': start,
                'count': count,
                'timeout': timeout,
            }
            start, count, timeout = update_summoner_history(s.account_id,
                                                            region,
                                                            queue[0],
                                                            days,
                                                            tts_data)
    logger.warning('Synced summoners in %s' % region.name)
    delete_obsolete_summoners(summoners=all_summoners, region=region)
    sync_end = time.time()
    timetotal = round((sync_end-sync_start)/60, 2)
    timeout = round(timeout/60, 2)
    logger.warning('Syncing %s finished at %s' % (region.name, time.ctime(
                                                    time.time())))
    logger.warning('Syncing %s took %s minutes to finish' % (
                                        region.name, str(timetotal)))
    logger.warning('Total timeout time was %s minutes' % (str(timeout)))


def sync_summoners():
    #regions = Region.objects.all()
    days = 1
    regions = Region.objects.filter(name='eun1')
    threads = [threading.Thread(target=update_region, args=(
                            region, days)) for region in regions]
    [x.start() for x in threads]
