# Script de démarrage rapide pour le projet Gestion PFE

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Projet Gestion PFE - ENSPD" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si le serveur est déjà en cours d'exécution
$process = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*venv*"}
if ($process) {
    Write-Host "Le serveur Django est déjà en cours d'exécution!" -ForegroundColor Yellow
    Write-Host "PID: $($process.Id)" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Voulez-vous l'arrêter et le redémarrer? (O/N)"
    if ($response -eq "O" -or $response -eq "o") {
        Stop-Process -Id $process.Id -Force
        Write-Host "Serveur arrêté." -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Le serveur continue de fonctionner." -ForegroundColor Green
        exit
    }
}

# Naviguer vers le répertoire du projet
Set-Location "c:\Users\hp\Documents\Projet gestion PFE"

Write-Host "Démarrage du serveur Django..." -ForegroundColor Green
Write-Host ""
Write-Host "URLs disponibles:" -ForegroundColor Yellow
Write-Host "  - Accueil:        http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  - Inscription:    http://127.0.0.1:8000/users/register/" -ForegroundColor White
Write-Host "  - Connexion:      http://127.0.0.1:8000/users/login/" -ForegroundColor White
Write-Host "  - Administration: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "Identifiants admin: admin / admin123" -ForegroundColor Magenta
Write-Host ""
Write-Host "Appuyez sur CTRL+C pour arrêter le serveur" -ForegroundColor Red
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Lancer le serveur
.\venv\Scripts\python.exe manage.py runserver
