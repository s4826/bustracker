# MBTA Bus Tracker
A basic bus tracking application that will display arrival times at bus stops
within the MBTA network.

Website: [https://www.mbtabustrackerapp.com](https://www.mbtabustrackerapp.com)

As an aside, some buses only run on select days (or not at all, after MBTA route
changes), and will therefore have no predictions.

## Installation
To download the app and install development dependencies, run:
```
git clone https://github.com/s4826/bustracker.git
cd bustracker
poetry install
```

## Running the app
To run the app, ```.env``` files are required to specify configuration values.
Examples can be found in the ```bustracker/env``` folder. If you just want to
test the application without any additional setup, do the following:
```
cp bustracker/env/env-example ./.env
cp bustracker/env/dev-env-example ./.env.dev
cp bustracker/env/test-env-example ./.env.test
flask run
```
Go to ```http://localhost:5000``` in a browser to use the app.

## Running the tests
To run the tests, only one command is needed, ```tox```. Depending on your
environment, you might not have all of the necessary Python versions to run
every test environment. There are various ways to configure ```tox``` to limit
the tests, but the easiest way to run the tests for an environment you know you
have is to run ```tox -e env```, where ```env``` is one of the environments
from ```tox.ini``` (i.e. lint, py39, etc...).

There are several tests which require MailHog running in a docker container.
Those tests are skipped if pytest can't access the mailhog server.
