from . import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "digdiscord",
        "USER": "root",
        "PASSWORD": "MOTDEPASSE1234",
        "HOST": "172.18.0.1",
        "PORT": "3306",
        "OPTIONS": {
            # Tell MySQLdb to connect with 'utf8mb4' character set
            "charset": "utf8mb4",
        },
        # Tell Django to build the test database with the 'utf8mb4' character set
        "TEST": {
#            "USER": "root",
            "NAME": "digdiscord_test",
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}
