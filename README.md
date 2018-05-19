##The Empty Ear Machine


### Installation
1. installing voices
Speech
(Main machine: Danish; E- English; O - Other)

2. installing necessary packages
`python --version`
Make sure it is python 3

`sudo easy_install pip`

`pip3 install --user pipenv`
http://docs.python-guide.org/en/latest/dev/virtualenvs/

packages in requirements.txt

brew install portaudio
pip3 install --upgrade google-api-python-client

3.Get the project folder
git clone https://github.com/cqx931/emptyEar

### Setup process
Master Machine
1. Check the ip -> change all three files
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://192.168.160.109:8080?role=master`
1. Run the server `sh mainMachine.bash`

Slave Machine I
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://192.168.160.109:8080?role=internationalA`
1. Run `sh intMachineA.bash` 

Slave Machine II
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://192.168.160.109:8080?role=internationalB`
1. Run `sh intMachineB.bash` 