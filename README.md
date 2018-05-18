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
1. Open IP:8080 in chrome browser without address bar
1. Run the server
1. Run mainEar.py on the same machine

Slave Machine I.
1. Open IP:8080 in chrome browser without address bar
1. Run `python subEar Dannish` 

Slave Machine II.
1. Open IP:8080 in chrome browser without address bar
1. Run `python subEar English`