# Run House Calculator GUI
# This script activates the virtual environment and runs the GUI application

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Launching House Calculator GUI..." -ForegroundColor Green
& .\venv\Scripts\python.exe house_calculator_gui.py

Write-Host "`nGUI closed." -ForegroundColor Green
