printf "\n%s\n\n" "Installing Chocolatey"
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
printf "\n%s\n\n" "Chocolatey installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing Python 3.6.7"
choco install python --version 3.7.2 --install-directory 'C:\Python36'
printf "\n%s\n\n" "Python 3.6.7 installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing VS Code"
choco install --install-directory 'C:\Program Files\Microsoft VS Code'
printf "\n%s\n\n" "VS Code installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing virtualenv"
pip install virtualenv
printf "\n%s\n\n" "virtualenv installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing virtualenvwrapper"
pip install virtualenvwrapper
printf "\n%s\n\n" "virtualenvwrapper installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing virtualenvwrapper-win"
pip install virtualenvwrapper-win
printf "\n%s\n\n" "virtualenvwrapper-win installed"
read -p "Press enter to continue"

printf "\n%s\n\n" "Creating vietualenv 'myenv'"
mkvirtualenv myenv
printf "\n%s\n\n" "'myenv' created"
read -p "Press enter to continue"

printf "\n%s\n\n" "working on myenv"
workon myenv
printf "\n%s\n\n" "In myenv"
read -p "Press enter to continue"

printf "\n%s\n\n" "Installing Requirements"
pip install -r requirements.txt
printf "\n%s\n\n" "Requirements installed"
read -p "Press enter to continue"

