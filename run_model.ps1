# Run House Model Script
# This script activates the virtual environment and runs the house model

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Running house model script..." -ForegroundColor Green
& .\venv\Scripts\python.exe houseModel.py

Write-Host "`nScript completed!" -ForegroundColor Green
