"""
Django settings for mugmailinglists project.

Generated by 'django-admin startproject' using Django 1.11.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import ldap
import saml2
import saml2.attributemaps
import saml2.saml
from corsheaders.defaults import default_methods
from django.utils.translation import ugettext_lazy as _
from django_auth_ldap.config import (
    GroupOfNamesType,
    LDAPSearch,
)
from docutils.core import publish_parts

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mailman API credentials
MAILMAN_REST_API_URL = 'http://localhost:8001'
MAILMAN_REST_API_USER = 'restadmin'

# Application definition

INSTALLED_APPS = [
    'hyperkitty',
    'postorius',
    'django_mailman3',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_gravatar',
    'paintstore',
    'compressor',
    'haystack',
    'django_extensions',
    'django_q',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'django_mailman3.lib.auth.fedora',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'django_mailman3.middleware.TimezoneMiddleware',
    'postorius.middleware.PostoriusMiddleware',
]

ROOT_URLCONF = 'mugmailinglists.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django_mailman3.context_processors.common',
                'hyperkitty.context_processors.common',
                'postorius.context_processors.postorius',
            ],
        },
    },
]

WSGI_APPLICATION = 'mugmailinglists.wsgi.application'


SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    'uid': ('username', ),
}
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    'xmlsec_binary': '/usr/bin/xmlsec1',

    # your entity id, usually your subdomain plus the url to the metadata view
    'entityid': 'http://localhost:8000/saml2/metadata/',

    # directory with attribute mapping
    'attribute_map_dir': os.path.dirname(saml2.attributemaps.__file__),

    # this block states what services we provide
    'service': {
        # we are just a lonely SP
        'sp': {
            'name': 'Federated Django sample SP',
            'name_id_format': saml2.saml.NAMEID_FORMAT_PERSISTENT,
            'endpoints': {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                'assertion_consumer_service': [
                    (
                        'http://localhost:8000/saml2/acs/',
                        saml2.BINDING_HTTP_POST
                    ),
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                'single_logout_service': [
                    (
                        'http://localhost:8000/saml2/ls/',
                        saml2.BINDING_HTTP_REDIRECT
                    ),
                    (
                        'http://localhost:8000/saml2/ls/post',
                        saml2.BINDING_HTTP_POST
                    ),
                ],
            },

            # attributes that this project need to identify a user
            'required_attributes': ['uid'],

            # attributes that may be useful to have but not required
            'optional_attributes': ['eduPersonAffiliation'],

            # in this section the list of IdPs we talk to are defined
            'idp': {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata

                # the keys of this dictionary are entity ids
                'https://localhost/simplesaml/saml2/idp/metadata.php': {
                    'single_sign_on_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SSOService.php',
                    },
                    'single_logout_service': {
                        saml2.BINDING_HTTP_REDIRECT: 'https://localhost/simplesaml/saml2/idp/SingleLogoutService.php',
                    },
                },
            },
        },
    },

    # where the remote metadata is stored
    'metadata': {
        'local': [os.path.join(BASE_DIR, 'remote_metadata.xml')],
    },

    # set to 1 to output debugging information
    'debug': 1,

    # Signing
    'key_file': os.path.join(BASE_DIR, 'mycert.key'),  # private part
    'cert_file': os.path.join(BASE_DIR, 'mycert.pem'),  # public part

    # Encryption
    'encryption_keypairs': [{
        'key_file': os.path.join(BASE_DIR, 'my_encryption_key.key'),  # private part
        'cert_file': os.path.join(BASE_DIR, 'my_encryption_cert.pem'),  # public part
    }],

    # own metadata settings
    'contact_person': [
        {
            'given_name': 'Lorenzo',
            'sur_name': 'Gil',
            'company': 'Yaco Sistemas',
            'email_address': 'lgs@yaco.es',
            'contact_type': 'technical'
        },
        {
            'given_name': 'Angel',
            'sur_name': 'Fernandez',
            'company': 'Yaco Sistemas',
            'email_address': 'angel@yaco.es',
            'contact_type': 'administrative'
        },
    ],
    # you can set multilanguage information here
    'organization': {
        'name': [
            ('Yaco Sistemas', 'es'),
            ('Yaco Systems', 'en'),
        ],
        'display_name': [
            ('Yaco', 'es'),
            ('Yaco', 'en'),
        ],
        'url': [
            ('http://www.yaco.es', 'es'),
            ('http://www.yaco.com', 'en'),
        ],
    },
    'valid_for': 24,  # how long is our metadata valid
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_auth_ldap.backend.LDAPBackend',
    'djangosaml2.backends.Saml2Backend',
)


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


AUTH_LDAP_SERVER_URI = "ldap://ldap.example.com"
AUTH_LDAP_BIND_DN = "cn=django-agent,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "phlebotinum"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=users,dc=example,dc=com", ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=django,ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}
AUTH_LDAP_PROFILE_ATTR_MAP = {
    "employee_number": "employeeNumber"
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
}
AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
}
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'de-at'

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # BASE_DIR + '/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)


# Django 1.6+ defaults to a JSON serializer, but it won't work with
# django-openid, see
# https://bugs.launchpad.net/django-openid-auth/+bug/1252826
#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'


LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'list_index'
LOGOUT_URL = 'account_logout'


#
# django-compressor
# https://pypi.python.org/pypi/django_compressor
#
COMPRESS_PRECOMPILERS = (
#   ('text/less', 'lessc {infile} {outfile}'),
#   ('text/x-scss', 'sassc -t compressed {infile} {outfile}'),
#   ('text/x-sass', 'sassc -t compressed {infile} {outfile}'),
    ('text/x-scss', 'sass -t compressed {infile} {outfile}'),
    ('text/x-sass', 'sass -t compressed {infile} {outfile}'),
#    ('text/x-sass', 'django_pyscss.compressor.DjangoScssFilter'),
#    ('text/x-scss', 'django_pyscss.compressor.DjangoScssFilter'),    
)


#
# Asynchronous tasks
#
Q_CLUSTER = {
    'timeout': 300,
    'save_limit': 100,
    'orm': 'default',
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'hyperkitty': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'postorius': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(process)d %(name)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
}


# Using the cache infrastructure can significantly improve performance on a
# production setup. This is an example with a local Memcached server.
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}


#
# HyperKitty-specific
#

# Only display mailing-lists from the same virtual host as the webserver
FILTER_VHOST = False


POSTORIUS_TEMPLATE_BASE_URL = 'http://localhost:8000'


if 'DJANGO_LOCAL_CONFIGURATION' in os.environ:
    filename = os.path.abspath(os.environ.get('DJANGO_LOCAL_CONFIGURATION'))
    if os.access(filename, os.R_OK):
        with open(filename) as config:
            code = compile(config.read(), filename, 'exec')
            exec(code, globals(), locals())
