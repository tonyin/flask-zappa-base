# flask-base

Base code for a new python flask web app

## Stack

* python3
* flask
* postgres
* sqlalchemy
* flask-migrate
* [bulma css](https://github.com/jgthms/bulma)
* [zappa](https://github.com/Miserlou/Zappa) (serverless deployment on aws)
* flask-s3 (static files from aws s3)

## Quickstart

0. Clone: `git clone https://github.com/tonyin/flask-base.git`
1. Set up virtualenv: `python3 -m venv venv` && `. venv/bin/activate`
2. Install libs: `pip install -r requirements.txt`
3. Create a config.env with required values (see config.py): `touch config.env`
4. Run: `./run.py`

## Deployment

TODO

### Static Assets

## Usage

### Database Migrations

1. `flask db migrate`
2. `flask db upgrade`

### Static Assets

Custom css and js modules can be defined in `app/static/css/app.css` and `app/static/js/app.js` respectively. We already load in bulma, jquery, and fontawesome.

### Accounts

This implementation is permissioned in that only allows Admins can add or remove users. A permissionless framework has open registration (form provided).

### Long Tasks

Lambda has a timeout of 30s, so longer-running tasks cannot be synchronously executed. To get around this, we asynchronously execute tasks with zappa's `@task` decorator. For an example, see the `email.py` function.

## References

* [explore flask](https://exploreflask.com/en/latest/index.html)
* [official flask](http://flask.pocoo.org/)
* [hack4impact/flask-base](https://github.com/hack4impact/flask-base)
