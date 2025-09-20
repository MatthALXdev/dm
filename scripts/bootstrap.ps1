param(
  [Parameter(Mandatory=$true)] [string] $DbPassword,
  [Parameter(Mandatory=$false)] [string] $DbName = "dm_db",
  [Parameter(Mandatory=$false)] [string] $DbUser = "dm_user",
  [Parameter(Mandatory=$false)] [string] $DbHost = "127.0.0.1",
  [Parameter(Mandatory=$false)] [string] $DbPort = "5432",
  [Parameter(Mandatory=$false)] [string] $StripePublic = "pk_test_xxx",
  [Parameter(Mandatory=$false)] [string] $StripeSecret = "sk_test_xxx"
)

# --- Helpers
function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

# --- 0) Pré-checks
Write-Step "Vérification Python"
$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { throw "Python introuvable dans PATH. Ouvre PowerShell avec 'python' disponible." }
python -V

# --- 1) Venv
Write-Step "Création/activation venv"
if (-not (Test-Path .\.venv)) { python -m venv .venv }
$PY = ".\.venv\Scripts\python.exe"
& $PY -V

# --- 2) Dépendances
Write-Step "Installation dépendances"
& $PY -m pip install --upgrade pip
& $PY -m pip install "Django>=5.1,<5.3" "psycopg[binary]>=3.1" stripe boto3 requests python-dotenv
& $PY -m pip install black flake8 pytest pytest-django
& $PY -m pip freeze | Out-File -Encoding UTF8 requirements.txt

# --- 3) Django project + app
Write-Step "Création projet Django + app core"
if (-not (Test-Path .\backend\manage.py)) {
  django-admin startproject backend .
}
if (-not (Test-Path .\core\apps.py)) {
  Push-Location backend
  & $PY manage.py startapp core
  Pop-Location
}

# --- 4) .env
Write-Step "Écriture .env"
@"
DJANGO_SECRET_KEY=$(New-Guid)-$(New-Guid)
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=$DbName
DB_USER=$DbUser
DB_PASSWORD=$DbPassword
DB_HOST=$DbHost
DB_PORT=$DbPort

STRIPE_PUBLIC_KEY=$StripePublic
STRIPE_SECRET_KEY=$StripeSecret
"@ | Out-File -Encoding UTF8 .\.env

# --- 5) settings.py (remplacement contrôlé)
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

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
"@ | Out-File -Encoding UTF8 $settingsPath

# --- 6) endpoint /health
Write-Step "Endpoint /health"
@"
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})
"@ | Out-File -Encoding UTF8 .\backend\core\views.py

# urls core (optionnel si besoin ultérieur)
if (-not (Test-Path .\backend\core\urls.py)) {
@"
from django.urls import path
from .views import health

urlpatterns = [
    path("health", health, name="health"),
]
"@ | Out-File -Encoding UTF8 .\backend\core\urls.py
}

# include dans urls racine
$urlsPath = ".\backend\backend\urls.py"
$urlsContent = Get-Content $urlsPath -Raw
if ($urlsContent -notmatch "include\(") {
  $urlsContent = $urlsContent -replace "from django.urls import path", "from django.urls import path, include"
}
if ($urlsContent -notmatch "core\.urls") {
  $urlsContent = $urlsContent -replace "urlpatterns = \[", "urlpatterns = [\n    path('', include('core.urls')),"
}
$urlsContent | Out-File -Encoding UTF8 $urlsPath

# --- 7) VS Code settings
Write-Step "VS Code .vscode/settings.json"
New-Item -ItemType Directory -Force -Path .\.vscode | Out-Null
@"
{
  "python.defaultInterpreterPath": ".venv\\Scripts\\python.exe",
  "python.analysis.typeCheckingMode": "basic",
  "editor.formatOnSave": true,
  "python.formatting.provider": "black"
}
"@ | Out-File -Encoding UTF8 .\.vscode\settings.json

# --- 8) .gitignore
Write-Step ".gitignore"
@"
# Python / Django
__pycache__/
*.py[cod]
*.sqlite3
*.log
/staticfiles/
/media/
/.env

# Venv
.venv/

# VS Code
.vscode/

# OS
.DS_Store
Thumbs.db
"@ | Out-File -Encoding UTF8 .\.gitignore

# --- 9) Migrations
Write-Step "Migrations"
Push-Location backend
& $PY manage.py makemigrations
& $PY manage.py migrate
Pop-Location

Write-Step "Bootstrap terminé 🎉"
Write-Host "Lance le serveur: .\.venv\Scripts\python.exe .\backend\manage.py runserver" -ForegroundColor Green
Write-Host "Test health: http://127.0.0.1:8000/health" -ForegroundColor Green

