# Enter the command below to run this script. Just copy and paste it into PowerShell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process -Force

#Download and install Chocolatey
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Refresh environment variables to recognize choco command, importing module is temporary, available in current session only 
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
& refreshenv

# Install Adobe DNG Converter using Chocolatey, overides current version if already installed
choco install adobe-dnc --force --yes