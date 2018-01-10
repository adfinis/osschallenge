![OSS Challenge Logo](/osschallenge/static/osschallenge/oss-challenge.jpg)

# OSS-Challenge

[![Build Status](https://travis-ci.org/adfinis-sygroup/osschallenge.svg?branch=master)](https://travis-ci.org/adfinis-sygroup/osschallenge)
[![codecov](https://codecov.io/gh/adfinis-sygroup/osschallenge/branch/master/graph/badge.svg)](https://codecov.io/gh/adfinis-sygroup/osschallenge)

A website for Open source tasks

## Installation
**Requirements**
* python 3.6.2
* docker
* docker-compose

If you have the requirements installed and configured,
you should be able to run the following commands:
```bash
$ git clone git@git.adfinis-sygroup.ch:ch-open/oss-challenge.src.git        # Clones the Git Repo into your present folder
$ cd oss-challenge.src                                                      # Moves into the folder
```
## Optional:
Setup an Pyenv/Virtualenv:
```bash
$ pyenv virtualenv 3.6.2 oss-challenge
$ pyenv local oss-challenge
```
 ____________________________________________________________________________________________________________

```bash
$ docker-compose up                                           # Starts the Docker containers
$ pip install -r requirements.txt                             # Installs requirements
$ pip install -r dev_requiremnts.txt                          # Installs Dev Requirements
$ python manage.py migrate                                    # Applies migrations
$ python manage.py loaddata osschallenge/fixture/*.json       # Loads all fixtures
$ python manage.py createsuperuser                            # Creates new Django superuser
```

Now you should be able to run:
```bash
$ python manage.py runserver        # Starts the localhost
```
and go to http://127.0.0.1:8000/ to get to the Website.

## License
Code released under the [GNU General Public License v3.0](LICENSE).
