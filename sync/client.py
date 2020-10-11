import requests
import logging
import time
import threading

from django.conf import settings

from summoners.models import (Summoner, Region, SummonerLeague,
                              SummonerHistory, SummonerSeries)


global logger
global conversions
global headers
global queues
global tiers
global divisions
global endpoints
global riot_api_url
global qcodes
global versions
global versions_url

headers = {'X-Riot-Token': settings.RIOT_TOKEN}
versions = settings.VERSIONS
qcodes = settings.QCODES
conversions = settings.CONVERSIONS
queues = settings.QUEUES
tiers = settings.TIERS
divisions = settings.DIVISIONS
endpoints = settings.RIOT_ENDPOINTS
riot_api_url = settings.RIOT_API_URL
versions_url = settings.VERSIONS_URL

logger = logging.getLogger(__name__)


# To be used by client over https per summoner
def get_summoner_by_name(name='', region_name=''):
    logger.info('Request data for summoner %s in region %s' % (name,
                                                               region_name))
    # http request to riot api returns json
    data = get_summoner(region_name=region_name, name=name)
    # Query db
    region = Region.objects.filter(name=region_name)
    if region.exists() and data is not None:
        region = region.get()
        clean_data = {(conversions[k] if k in conversions.keys() else k
                       ): v for k, v in data.items()}
        clean_data['region'] = region
        summoner = create_summoner(data=clean_data)
        update_summoner_history(summoner=summoner, region_name=region.name)
        # Get league for summoner
        league_data = get_league(region_name=region.name,
                                 summoner_id=summoner.summoner_id,
                                 endpoint=endpoints['league'])
        temp = [{(conversions[k] if k in conversions.keys() else k
                  ): v for k, v in each.items()} for each in league_data]
        leagues = [{k: v for k, v in each.items(
                                ) if k not in (
                    'mini_series', 'summoner_id', 'name')}for each in temp]
        for league in leagues:
            league['summoner'] = summoner
            create_league(data=league)
        return summoner
    else:
        logger.warning('No data for summoner %s in region %s' % (
                                            name, region_name))
        return None


def get_summoner_by_league(league_data=None, region=None):
    summoner_id = league_data['summonerId']
    data = get_summoner(region_name=region.name, summoner_id=summoner_id)
    if data is not None and league_data is not None:
        clean_data = {(conversions[k] if k in conversions.keys() else k
                       ): v for k, v in data.items()}
        clean_data['region'] = region
        summoner = create_summoner(data=clean_data)
        update_summoner_history(summoner=summoner, region_name=region.name)
        temp = {(conversions[k] if k in conversions.keys() else k
                 ): v for k, v in league_data.items()}
        league = {k: v for k, v in temp.items(
                                        ) if k not in (
                                        'mini_series', 'summoner_id', 'name')}
        league['summoner'] = summoner
        create_league(data=league)
        return summoner
    else:
        logger.warning('No data for summoner %s in region %s' % (
                                            summoner_id, region.name))
        return None


def get_summoner_history(account_id='', region_name=''):
    url = 'https://%s.%s%s%s' % (
        region_name, riot_api_url, endpoints['summoner_history'], account_id)
    histories = []
    for qcode in qcodes.keys():
        params = {
            'beginTime': int(time.time() - 604800),
            'endIndex': 100,
            'queue': qcode,
        }
        response = requests.get(url, headers=headers, params=params)
        logger.info('Request send to %s' % url)
        if response.status_code != 200:
            logger.error('Response message: %s' % response.json(
                                        )['status']['message'])
            continue
        else:
            histories += response.json()['matches']
    return histories


def update_summoner_history(summoner=None, region_name=''):
    logger.info('Updating history for summoner %s' % summoner.summoner_id)
    data = get_summoner_history(account_id=summoner.account_id,
                                region_name=region_name)
    if len(data) > 0:
        temp = [{(conversions[k] if k in conversions.keys() else k
                  ): v for k, v in each.items(
                )} for each in data]
        temp = [{k: v for k, v in each.items(
                    ) if k not in ('platformId', 'season')} for each in temp]
        clean_data = [{k: (qcodes[v] if k == 'queue' else v
                           ) for k, v in each.items()} for each in temp]
        [SummonerHistory.objects.get_or_create(summoner=summoner, **m
                                               ) for m in clean_data]
        logger.info('History updated for summoner %s' % summoner.summoner_id)
    else:
        logger.warning('No history found for summoner %s' %
                       summoner.summoner_id)


def get_summoner(region_name='', summoner_id=None, name=None):
    if summoner_id is None and name is not None:
        endpoint = endpoints['summoner_by_name']
        param = name
    elif name is None and summoner_id is not None:
        endpoint = endpoints['summoner_by_id']
        param = summoner_id
    else:
        return None
    url = 'https://%s.%s%s%s' % (
                                region_name,
                                riot_api_url,
                                endpoint,
                                param)
    logger.info('Request send to %s' % url)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error('Response message: %s' % response.json(
                                        )['status']['message'])
        return None
    else:
        return response.json()


def get_league(region_name='', endpoint='', queue='',
               tier='', division='', summoner_id=None):
    if summoner_id is not None:
        url = 'https://%s.%s%s%s/' % (
                                region_name,
                                riot_api_url,
                                endpoint,
                                summoner_id
                                      )
    else:
        url = 'https://%s.%s%s%s/%s/%s' % (
                                    region_name,
                                    riot_api_url,
                                    endpoint,
                                    queue,
                                    tier,
                                    division)
    logger.info('Request send to %s' % url)
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        logger.error('Response message: %s' % response.json(
                                        )['status']['message'])
        return None
    else:
        return response.json()


def get_divisionless_league(region_name='', endpoint='', queue=''):
    url = 'https://%s.%s%sby-queue/%s' % (
                                region_name,
                                riot_api_url,
                                endpoint,
                                queue)
    logger.info('Request send to %s' % url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logger.warning('Response message: %s' % response.json(
                                        )['status']['message'])
        return None
    else:
        return convert_divisionless_league(response.json())


def get_leagues(region_name='', queue='', tier=''):
    logger.info('Requesting league(s) data for %s %s %s' %
                (region_name, queue, tier))
    leagues = []
    if tier not in ('CHALLENGER', 'GRANDMASTER', 'MASTER'):
        for division in divisions:
            league = get_league(
                region_name,
                endpoints['leagues'],
                queue,
                tier,
                division[0])
            if league is not None:
                leagues += league
            else:
                logger.error(
                    'Dropped %s %s %s because league is %s' % (
                        queue, tier,  division, str(league)))
    else:
        league = get_divisionless_league(
                        region_name,
                        endpoints[tier.lower()],
                        queue)
        if league is not None:
            leagues += league
        else:
            logger.error(
                'Dropped %s %s because league is %s' % (
                        queue, tier, str(league)))
    logger.info('Got league(s) data for %s %s %s' %
                (region_name, queue, tier))
    return leagues


def convert_divisionless_league(data=None):
    if data is None:
        logger.error('Cannot convert because data %s' % str(data))
        return []
    common = {k: v for k, v in data.items() if k not in ('entries',)}
    league = [{**common, **each} for each in data['entries']]
    return league


def create_regions(data=None):
    regions = []
    for each in data:
        url = versions_url + versions[each[0]] + '.json'
        response = requests.get(url)
        version = response.json()['v']
        region = Region.objects.filter(name=each[0])
        if region.exists():
            region.update(version=version)
            regions.append(region.get())
        else:
            regions.append(Region.objects.create(name=each[0],
                                                 version=version))
    logger.warning('Created all regions')
    return regions


def extract_summoner_series(data=None):
    series = [{k: v for k, v in each.items() if k in (
                    'miniSeries', 'summonerId')} for each in data]
    logger.info('Got summoner mini series')
    return series


def create_summoner(data=None):
    logger.info('Creating summoner %s in region %s' %
                (data['summoner_id'], data['region'].name))

    old_summoner = Summoner.objects.filter(summoner_id=data['summoner_id'],
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


def create_league(data=None):
    logger.info('Creating league for summoner %s in queue %s' %
                (data['summoner'].summoner_id, data['queue']))

    old_league = SummonerLeague.objects.filter(summoner=data['summoner'],
                                               queue=data['queue'],)
    if old_league.exists():
        old_league.update(**data)
        logger.info('Created league for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, data['queue']))
    else:
        SummonerLeague.objects.create(**data)
        logger.info('Created league for summoner %s in queue %s' %
                    (data['summoner'].summoner_id, data['queue']))


def delete_obsolete_summoners(summoners=[], region=None):
    all_summoners = Summoner.objects.filter(region=region)
    [s.delete() for s in all_summoners if s not in summoners]
    logger.warning('Deleted obsolete summoners on region %s' % region.name)


def update_region(region=None):
    summoners = []
    logger.warning('Syncing %s at %s' % (region.name, time.ctime(time.time())))
    sync_start = time.time()
    timeout = 0
    for queue in queues:
        for tier in tiers:
            logger.warning('Syncing %s %s %s' % (
                                    region.name, queue[0], tier[0]))
            count = 0
            elapsed = 0
            start = time.time()
            data = get_leagues(
                    region_name=region.name, queue=queue[0], tier=tier[0])
            if tier[0] in ('GRANDMASTER', 'MASTER', 'CHALLENGER'):
                count += 1
            else:
                count += 4
            for each in data:
                elapsed = time.time() - start
                if count + 3 > 100 and elapsed <= 120:
                    tts = round(120 - elapsed)
                    timeout += tts
                    logger.warning(
                        'Pausing sync in region %s for %s seconds' %
                        (region.name, str(tts)))
                    time.sleep(tts)
                    count = 0
                    start = time.time()
                    logger.warning('Resuming sync in region %s' % region.name)
                count += 3
                summoners.append(get_summoner_by_league(league_data=each,
                                                        region=region))
            logger.warning('Finished syncing %s %s %s' % (
                                    region.name, queue[0], tier[0]))
    delete_obsolete_summoners(summoners=summoners, region=region)
#        summoners_series = extract_summoner_series(leagues)
    sync_end = time.time()
    timetotal = round((sync_end-sync_start)/60, 2)
    timeout = round(timeout/60, 2)
    logger.warning('Syncing %s finished at %s' % (region.name, time.ctime(
                                                    time.time())))
    logger.warning('Syncing %s took %s minutes to finish' % (
                                        region.name, str(timetotal)))
    logger.warning('Total timeout time was %s minutes' % (str(timeout)))


def sync_data_dragon():
    regions = settings.REGIONS
    regions = create_regions(regions)


def sync_summoners():
    regions = Region.objects.all()
    threads = [threading.Thread(target=update_region, args=(
                            region,)) for region in regions]
    [x.start() for x in threads]
