Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
& refreshenv
choco install adobe-dnc -y # Downloading stuck at 4% of dowloading :(