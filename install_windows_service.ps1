# Install and configure the RemoveBG service
$serviceName = "RemoveBGService"
$workingDirectory = "C:\Users\Computador\Documents\programming\remove_bg"
$virtualEnvPath = Join-Path $workingDirectory ".venv\Scripts\pythonw.exe"
$wsgiPath = Join-Path $workingDirectory "wsgi.py"
$scriptPath = Join-Path $workingDirectory "run_service.ps1"

# Environment variables for the service
$env:PYTHONPATH = $workingDirectory
$env:FLASK_ENV = "production"
$env:FLASK_APP = "wsgi.py"
$env:VIRTUAL_ENV = Join-Path $workingDirectory ".venv"
$env:PATH = "$env:VIRTUAL_ENV\Scripts;$env:PATH"

# Check if running as administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "Please run this script as Administrator"
    exit 1
}

# Create the service using NSSM (Non-Sucking Service Manager)
Write-Host "Downloading NSSM..."
$nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
$nssmZip = Join-Path $workingDirectory "nssm.zip"
$nssmPath = Join-Path $workingDirectory "nssm"

# Download and extract NSSM
Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
Expand-Archive -Path $nssmZip -DestinationPath $nssmPath -Force
Remove-Item $nssmZip

# Use the appropriate architecture
$nssmExe = Join-Path $nssmPath "nssm-2.24\win64\nssm.exe"

# Remove existing service if it exists
& $nssmExe stop $serviceName
& $nssmExe remove $serviceName confirm

# Install the new service
Write-Host "Installing service..."
& $nssmExe install $serviceName $virtualEnvPath $wsgiPath
& $nssmExe set $serviceName AppDirectory $workingDirectory
& $nssmExe set $serviceName DisplayName "Remove BG Service"
& $nssmExe set $serviceName Description "Background removal service using Flask and Waitress"
& $nssmExe set $serviceName Start SERVICE_AUTO_START
& $nssmExe set $serviceName AppStdout (Join-Path $workingDirectory "logs\service.log")
& $nssmExe set $serviceName AppStderr (Join-Path $workingDirectory "logs\error.log")
& $nssmExe set $serviceName AppEnvironmentExtra "PYTHONPATH=$workingDirectory" "FLASK_ENV=production" "FLASK_APP=wsgi.py"
& $nssmExe set $serviceName AppThrottle 5000
& $nssmExe set $serviceName AppStopMethodSkip 0
& $nssmExe set $serviceName AppStopMethodConsole 1000
& $nssmExe set $serviceName AppRestartDelay 5000

# Create logs directory
New-Item -ItemType Directory -Force -Path (Join-Path $workingDirectory "logs")

# Start the service
Write-Host "Starting service..."
Start-Service $serviceName

Write-Host "Service installed and started successfully!"
Write-Host "You can manage the service using:"
Write-Host "Start-Service $serviceName"
Write-Host "Stop-Service $serviceName"
Write-Host "Restart-Service $serviceName"
Write-Host "Get-Service $serviceName"

# Open the service manager
Write-Host "Opening Services..."
services.msc
