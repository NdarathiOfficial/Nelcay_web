"""
Django settings for Nelcay project.
"""

from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path

DEBUG = False

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# Wrapped in os.environ to allow Vercel to inject a secure key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-w%w-tn0^99eu&50cwnh)=c%56))@mc3s=#fofw7jl76t+g7glq')



ALLOWED_HOSTS = [
    'nelcay-web-pi.vercel.app',
    'nelcay-e7uqogiyu-ndarathi-s-projects.vercel.app', # Add your specific deployment URL here
    '.vercel.app',
    'localhost',
    '127.0.0.1'
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'django_daraja',
    'anymail',  # Required for SendGrid integration
    # Local apps
    'system',
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

ROOT_URLCONF = 'Nelcay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'system/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Nelcay.wsgi.application'

# Database
# Note: SQLite will reset on Vercel. Consider Postgres (e.g., Supabase, Neon) for production.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Where Django looks for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# CRITICAL FOR VERCEL: Where collectstatic dumps the files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# M-PESA DARAJA SETTINGS
# ==========================================
MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT', 'sandbox')
MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY', 'NJgzS0YN2vQFcAYKQKIiZgL1eEhmAKWTgnhjesz6xGngIv3U')
MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET', 'iYtll0bf38Mz4JAYnsiEgoCd8x8p7GhhkIp9I8Xnf94afAxHh4ky8r8k0Njp5e3J')
MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE', '5457007')
MPESA_EXPRESS_SHORTCODE = os.environ.get('MPESA_EXPRESS_SHORTCODE', '174379')
MPESA_SHORTCODE_TYPE = os.environ.get('MPESA_SHORTCODE_TYPE', 'lipa na mpesa')
MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')


# ==========================================
# EMAIL & SENDGRID SETTINGS
# ==========================================
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

# The API key must be injected via Vercel's Environment Variables dashboard
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get("SENDGRID_API_KEY"),
}

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "Nelcay Cakey Treats <nelcaycakeytreats@gmail.com>"
)

CONTACT_RECEIVER_EMAIL = os.environ.get(
    "CONTACT_RECEIVER_EMAIL", "nelcaycakeytreats@gmail.com"
)