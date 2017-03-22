# How to install

1. '''git clone git@git.adfinis-sygroup.ch:ch-open/oss-challenge.src.git'''
2. '''docker-compose up'''
3. set up pyenv/virtualenv
3. '''pip install -r requirements.txt'''
4. '''python manage.py migrate'''
5. '''python manage.py loaddata osschallenge/fixture/role.json'''
6. '''python manage.py createsuperuser'''
