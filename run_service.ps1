# Get the current directory
$workingDirectory = "C:\Users\Computador\Documents\programming\remove_bg"
$virtualEnvPath = Join-Path $workingDirectory ".venv"

# Set environment variables
$env:PYTHONPATH = $workingDirectory
$env:FLASK_ENV = "production"
$env:FLASK_APP = "wsgi.py"
$env:VIRTUAL_ENV = $virtualEnvPath
$env:PATH = "$virtualEnvPath\Scripts;$env:PATH"

Write-Host "Starting Remove BG Service..."
Write-Host "Working Directory: $workingDirectory"

# Activate virtual environment
& "$virtualEnvPath\Scripts\Activate.ps1"

# Create necessary directories if they don't exist
python -c "from util.setup_dirs import setup_directories; setup_directories()"

# Start the application using Waitress
python "$workingDirectory\wsgi.py"

Write-Host "Service is running at http://localhost:8000"
