# flask-base

Base code for any python flask web apps. Expect it to be constantly evolving and have a lot of sample code.

## Docs

### Quickstart

1. `git clone https://github.com/tonyin/flask-base.git`
2. `cd flask-base`
3. `virtualenv venv`
4. `. venv/bin/activate`
5. `pip install -r requirements.txt`
6. `cp instance/sample-config.py instance/config.py`
7. `./run.py`

### Deployment

0. Set up Nginx reverse proxy
1. `cd flask-base`
2. `. venv/bin/activate`
3. `pip install gunicorn`
4. `gunicorn app:app -p app.pid -D`
5. ``kill `cat app.pid` `` (to stop)

## References

I made this repo to reuse over and over again in my other web apps. It uses ideas from multiple sources:

- [explore flask](https://exploreflask.com/en/latest/index.html)
- [official flask](http://flask.pocoo.org/)
