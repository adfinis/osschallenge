# How to install

```bash
git clone git@git.adfinis-sygroup.ch:ch-open/oss-challenge.src.git
cd oss-challenge.src
pyenv virtualenv 2.7 oss-challenge
pyenv local oss-challenge
pip install -r requirements.txt
docker-compose up
python manage.py migrate
python manage.py loaddata osschallenge/fixture/role.json
python manage.py createsuperuser
```
