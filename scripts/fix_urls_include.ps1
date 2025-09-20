function Write-Step($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

Write-Step "Correction de backend/urls.py pour ajouter 'include'"

$urlsPath = ".\backend\urls.py"
$urlsContent = Get-Content $urlsPath -Raw

# Si 'include' n'est pas présent dans l'import, on le rajoute
if ($urlsContent -match "from django.urls import path" -and $urlsContent -notmatch "include") {
    $urlsContent = $urlsContent -replace "from django.urls import path", "from django.urls import path, include"
}

$urlsContent | Out-File -Encoding UTF8 $urlsPath

Write-Step "Correction terminée ✅"
Write-Host "Relance les migrations : .\\.venv\\Scripts\\python.exe manage.py makemigrations && .\\.venv\\Scripts\\python.exe manage.py migrate"
