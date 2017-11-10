# OSS-Challenge

A website for Opensource tasks

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

Open a second console and run:
```bash
$ docker-compose up         # Starts the Docker containers
```

Switch back to your old console and continue with:
```bash
$ pip install -r requirements.txt                             # Installes all requirements
$ python manage.py migrate                                    # Applies migrations
$ python manage.py loaddata osschallenge/fixture/role.json    # Loads role fixtures
$ python manage.py loaddata osschallenge/fixture/rank.json    # Loads rank fixtures
$ python manage.py createsuperuser                            # Creates new Django superuser
$ python manage.py delete_quarter_ranks
# Cronjob who deletes the quarter_points in the profile model every quarter
```

Now you should be able to run:
```bash
$ python manage.py runserver        # Starts the localhost
```
and go to http://127.0.0.1:8000/ to get to the Website.
