# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # CORS headers
    "corsheaders",
    # Django rest framework
    "rest_framework",
    # My installed apps
    "recipes",
    "authors",
    "tag",
]
