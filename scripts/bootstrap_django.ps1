param(
    [Parameter(Mandatory = $true)] [string] $DbPassword,
    [Parameter(Mandatory = $false)] [string] $DbName = "dm_db",
    [Parameter(Mandatory = $false)] [string] $DbUser = "dm_user",
    [Parameter(Mandatory = $false)] [string] $DbHost = "127.0.0.1",
    [Parameter(Mandatory = $false)] [string] $DbPort = "5432"
)

function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

# --- 0) Vérification Django
Write-Step "Vérification Django"
& .\.venv\Scripts\python.exe -m django --version

# --- 1) Création projet Django + app core
Write-Step "Création projet Django + app core"
if (-not (Test-Path .\backend\manage.py)) {
    & .\.venv\Scripts\python.exe -m django startproject backend .
}
if (-not (Test-Path .\backend\core\apps.py)) {
    Push-Location backend
    & ..\.venv\Scripts\python.exe manage.py startapp core
    Pop-Location
}

# --- 2) settings.py
Write-Step "Configuration settings.py"
$settingsPath = ".\backend\backend\settings.py"
@"
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR.parent / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "dm_db"),
        "USER": os.getenv("DB_USER", "dm_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"@ | Out-File -Encoding UTF8 $settingsPath

# --- 3) Endpoint /health
Write-Step "Ajout endpoint /health"
@"
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
"@ | Out-File -Encoding UTF8 .\backend\core\views.py

@"
from django.urls import path
from .views import health

urlpatterns = [
    path("health", health, name="health"),
]
"@ | Out-File -Encoding UTF8 .\backend\core\urls.py

# --- 4) Injection core.urls dans urls.py
$urlsPath = ".\backend\backend\urls.py"
$urlsContent = Get-Content $urlsPath -Raw
if ($urlsContent -notmatch "include\(") {
    $urlsContent = $urlsContent -replace "from django.urls import path", "from django.urls import path, include"
}
if ($urlsContent -notmatch "core\.urls") {
    $urlsContent = $urlsContent -replace "urlpatterns = \[", "urlpatterns = [`n    path('', include('core.urls')),"
}
$urlsContent | Out-File -Encoding UTF8 $urlsPath

# --- 5) Migrations
Write-Step "Migrations"
Push-Location backend
& ..\.venv\Scripts\python.exe manage.py makemigrations
& ..\.venv\Scripts\python.exe manage.py migrate
Pop-Location

Write-Step "Bootstrap Django terminé 🎉"
Write-Host "Lance le serveur: .\\.venv\\Scripts\\python.exe .\\backend\\manage.py runserver" -ForegroundColor Green
Write-Host "Test health: http://127.0.0.1:8000/health" -ForegroundColor Green
