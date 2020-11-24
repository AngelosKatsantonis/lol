from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''
RIOT_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'sync',
    'summoners',
    'game_assets',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['lol/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'lol.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lol',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Athens'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_ROOT = '/public/'

from .local_settings import *  # noqa

QUEUES = [

    ('RANKED_SOLO_5x5', '5v5 Ranked Solo games'),
    ('RANKED_FLEX_SR', '5v5 Ranked Flex games'),
    ('ARAM', '5v5 ARAM games')
]

QCODES = {
    'RANKED_SOLO_5x5': 420,
    'RANKED_FLEX_SR': 440,
    'ARAM': 450,
}

QCODES_REVERSE = {
    420: 'RANKED_SOLO_5x5',
    440: 'RANKED_FLEX_SR',
    450: 'ARAM',
}

MASTER_TIERS = [
    ('CHALLENGER', 'Challenger'),
    ('GRANDMASTER', 'Grandmaster'),
    ('MASTER', 'Master'),
]

TIERS = [
    ('DIAMOND', 'Diamond'),
    ('PLATINUM', 'Platinum'),
    ('GOLD', 'Gold'),
    ('SILVER', 'Silver'),
    ('BRONZE', 'Bronze'),
    ('IRON', 'Iron'),
]

DIVISIONS = [
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
]

REGIONS = [
    ('br1', 'Brazil'),
    ('eun1', 'Europe Nordic & East'),
    ('euw1', 'Europe West'),
    ('jp1', 'Japan'),
    ('la1', 'Latin America North'),
    ('la2', 'Latin America South'),
    ('na1', 'North America'),
    ('oc1', 'Oceania'),
    ('ru', 'Russia'),
    ('tr1', 'Turkey'),
    ('kr', 'Republic of Korea'),
]


RIOT_ENDPOINTS = {
    'league': '/lol/league/v4/entries/by-summoner/',
    'leagues': '/lol/league/v4/entries/',
    'master': '/lol/league/v4/masterleagues/',
    'grandmaster': '/lol/league/v4/grandmasterleagues/',
    'challenger': '/lol/league/v4/challengerleagues/',
    'summoner_by_name': '/lol/summoner/v4/summoners/by-name/',
    'summoner_by_id': '/lol/summoner/v4/summoners/',
    'summoner_by_account': '/lol/summoner/v4/summoners/by-account/',
    'summoner_history': '/lol/match/v4/matchlists/by-account/',
    'match': '/lol/match/v4/matches/',
    'timeline': '/lol/match/v4/timelines/by-match/',
}

RIOT_API_URL = 'api.riotgames.com'

CONVERSIONS = {
    'summonerId': 'summoner_id',
    'summonerName': 'name',
    'leagueId': 'league_id',
    'queueType': 'queue',
    'leaguePoints': 'league_points',
    'freshBlood': 'fresh_blood',
    'hotStreak': 'hot_streak',
    'rank': 'division',
    'miniSeries': 'mini_series',
    'accountId': 'account_id',
    'profileIconId': 'icon',
    'revisionDate': 'revision',
    'summonerLevel': 'level',
    'id': 'summoner_id',
    'gameId': 'game_id',
}

VERSIONS = {
    'br1': 'br',
    'eun1': 'eune',
    'euw1': 'euw',
    'jp1': 'jp',
    'la1': 'lan',
    'la2': 'las',
    'na1': 'na',
    'oc1': 'oce',
    'ru': 'ru',
    'tr1': 'tr',
    'kr': 'kr',
}

VERSIONS_URL = 'https://ddragon.leagueoflegends.com/realms/'
ALL_CHAMPIONS_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json'
CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champion}.json'
CHAMPION_SQUARE_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{full}'
CHAMPION_SPELL_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{full}'
CHAMPION_PASSIVE_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/passive/{full}'

SPELL_KEYBINDS = {
    0: 'q',
    1: 'w',
    2: 'e',
    3: 'r',
}

SUMMONER_SPELLS_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/summoner.json'
SUMMONER_SPELL_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{full}'

ITEMS_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json'
ITEM_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{full}'

SUMMONER_ICONS_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/profileicon.json'
SUMMONER_ICON_URL = 'http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{full}'

SUMMONER_POSITIONS = [
    ('TOP', 'Top'),
    ('MID', 'Mid'),
    ('JUNGLE', 'Jungle'),
    ('BOT', 'Bot'),
    ('SUPPORT', 'Support'),
]
