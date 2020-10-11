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

from .local_settings import *  # noqa

QUEUES = [

    ('RANKED_SOLO_5x5', '5v5 Ranked Solo games'),
]

QCODES = {
    420: 'RANKED_SOLO_5x5',
}
'''
TIERS = [
    ('RANKED_FLEX_SR', '5v5 Ranked Flex games'),
    440: 'RANKED_FLEX_SR'
    ('CHALLENGER', 'Challenger'),
    ('GRANDMASTER', 'Grandmaster'),
    ('MASTER', 'Master'),
    ('DIAMOND', 'Diamond'),
    ('PLATINUM', 'Platinum'),
    ('GOLD', 'Gold'),
    ('SILVER', 'Silver'),
    ('BRONZE', 'Bronze'),
    ('IRON', 'Iron'),
]
'''
TIERS = [
    ('CHALLENGER', 'Challenger'),
    ('DIAMOND', 'Diamond'),
]

DIVISIONS = [
    ('I', 'I'),
    ('II', 'II'),
    ('III', 'III'),
    ('IV', 'IV'),
]
'''
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
'''
REGIONS = [
    ('eun1', 'Europe Nordic & East'),
    ('euw1', 'Europe West'),
]


RIOT_ENDPOINTS = {
    'league': '/lol/league/v4/entries/by-summoner/',
    'leagues': '/lol/league/v4/entries/',
    'master': '/lol/league/v4/masterleagues/',
    'grandmaster': '/lol/league/v4/grandmasterleagues/',
    'challenger': '/lol/league/v4/challengerleagues/',
    'summoner_by_name': '/lol/summoner/v4/summoners/by-name/',
    'summoner_by_id': '/lol/summoner/v4/summoners/',
    'summoner_history': '/lol/match/v4/matchlists/by-account/',
    'queue_codes':
    'http://static.developer.riotgames.com/docs/lol/queues.json',
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
