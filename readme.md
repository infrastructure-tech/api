# Web API For Infrastructure.Tech

![build](https://github.com/infrastructure-tech/api/actions/workflows/docker-build.yml/badge.svg)
![tests](https://github.com/infrastructure-tech/api/actions/workflows/django-unit-tests.yml/badge.svg)

## Initial Setup

### Notes

* OS is assumed to be Ubuntu 20.04 or a suitable alternative
* To make it easy to copy code, permissions have been left out. If you have questions about permissions, ask eons.

### Setup Postgresql

If you don't have postgresql installed, you can install it with:
`apt install postgresql postgresql-contrib`

make sure postgress is running on localhost with the following:
`ss -tulnp | grep 5432`
This should output something like:
`tcp     LISTEN   0        244            127.0.0.1:5432           0.0.0.0:* `

Postgress can be controlled via systemd. i.e.
```
systemctl enable postgresql
systemctl disable postgresql
systemctl start postgresql
systemctl stop postgresql
systemctl restart postgresql
```

To setup postgres, run the following:
```
source ./api.env
cat << EOF > ./pg-setup.sql
CREATE DATABASE $API_PG_DB;
CREATE USER $API_PG_USER WITH ENCRYPTED PASSWORD '$API_PG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $API_PG_DB TO $API_PG_USER;
ALTER ROLE $API_PG_USER SET client_encoding TO 'utf8';
ALTER ROLE $API_PG_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $API_PG_USER SET timezone TO 'UTC';
EOF
chown postgres:postgres ./pg-setup.sql
sudo -u postgres psql -f ./pg-setup.sql
```

### Libpq

If libpq is not installed, run:
`apt install libpq-dev`

### Check Python Version

`python3 --version`

If this is anything less than 3.7, upgrade python
You can install python with something like:
`apt install python-3.9`

NOTE: if you still get 3.6..., etc. when running `python3 --version`, you may need to run something like the following (adapt for your system if necessary):
```
rm /usr/bin/python3
ln -s /usr/bin/python3.9 /usr/bin/python3
```

### Install Virtual Environment

If virtualenv is not installed, install it through apt:
`apt install virtualenv`

```
virtualenv venv
source ./venv/bin/activate
python -m pip install pip -U
pip install -r requirements.txt
```

## Run Django

```
source ./venv/bin/activate
source ./api.env
cd ./api_project
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py runserver
```

