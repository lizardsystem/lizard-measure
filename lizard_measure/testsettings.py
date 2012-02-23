import os
from lizard_ui.settingshelper import setup_logging

# SETTINGS_DIR allows media paths and so to be relative to this settings file
# instead of hardcoded to c:\only\on\my\computer.
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))

# BUILDOUT_DIR is for access to the "surrounding" buildout, for instance for
# BUILDOUT_DIR/var/static files to give django-staticfiles a proper place
# to place all collected static files.
BUILDOUT_DIR = os.path.abspath(os.path.join(SETTINGS_DIR, '..'))

LOGGING = setup_logging(BUILDOUT_DIR)

DEBUG = True
TEMPLATE_DEBUG = True

# Django supports the databases 'postgresql_psycopg2', 'postgresql', 'mysql',
# 'sqlite3' and 'oracle'. If you use a geodatabase, Django supports the
# following ones:
#
#   'django.contrib.gis.db.backends.postgis'
#   'django.contrib.gis.db.backends.mysql'
#   'django.contrib.gis.db.backends.oracle'
#   'django.contrib.gis.db.backends.spatialite'

DATABASES = {
    'default': {
        'NAME': os.path.join(BUILDOUT_DIR, 'lizard-measure.db'),
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'USER': 'buildout',
        'PASSWORD': 'buildout',
        'HOST': '',  # empty string for localhost.
        'PORT': '',  # empty string for default.
        }
    }

SITE_ID = 1
INSTALLED_APPS = [
    'south',
    'lizard_map',
    'lizard_ui',
    'lizard_security',
    'lizard_geo',
    'lizard_area',
    'lizard_graph',
    'lizard_history',
    'lizard_measure',
    'django_extensions',
    'staticfiles',
    'compressor',
    'django_nose',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    ]
ROOT_URLCONF = 'lizard_measure.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Used for django-staticfiles
STATIC_URL = '/static_media/'
TEMPLATE_CONTEXT_PROCESSORS = (
    # Default items.
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    # Needs to be added for django-staticfiles to allow you to use
    # {{ STATIC_URL }}myapp/my.css in your templates.
    'staticfiles.context_processors.static_url',
    )

SOUTH_TESTS_MIGRATE = False

try:
    # Import local settings that aren't stored in svn.
    from lizard_measure.local_testsettings import *
except ImportError:
    pass
