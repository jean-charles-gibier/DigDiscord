from . import *
import os
import pprint

# Production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get('PRODUCTION_BD_NAME'),
        "USER": os.environ.get('PRODUCTION_BD_USER'),
        "PASSWORD": os.environ.get('PRODUCTION_BD_PWD'),
        "HOST": os.environ.get('PRODUCTION_BD_HOST'),
        "PORT": os.environ.get('PRODUCTION_BD_PORT'),
        "OPTIONS": {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            "charset": "utf8mb4",
        },
        # Tell Django to build the test database with the 'utf8mb4' character set
        "TEST": {
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
             "USER": "rout",
            "NAME": "digdiscord_test",
#           "PASSWORD": "MOTDEPASSE1234",
        },
    }
}


ALLOWED_HOSTS.append("tgpa8220.odns.fr")
STATIC_ROOT = os.path.join(BASE_DIR, 'dumps')
