# How to install

```bash
git clone git@git.adfinis-sygroup.ch:ch-open/oss-challenge.src.git
cd oss-challenge.src
pyenv virtualenv 3.6.2 oss-challenge
pyenv local oss-challenge
pip install -r requirements.txt
docker-compose up
python manage.py migrate
python manage.py loaddata osschallenge/fixture/role.json
python manage.py loaddata osschallenge/fixture/rank.json
python manage.py createsuperuser
python manage.py delete_quarter_ranks (cronjob who deletes the quarter_points in the profile model every quarter)
```
