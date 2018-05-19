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
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=IP:8080`
1. Run the server `python server/app.py`
1. Run `python mainEar.py` on the same machine
1. Run `python subEar danish` 

Slave Machine I.
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=IP:8080`
1. Run `python subEar international` 

Slave Machine II.
1. Open Visual client in chrome browser without address bar `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=IP:8080`
1. Run `python subEar english`