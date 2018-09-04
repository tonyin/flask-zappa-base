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

## Configuration

### Environments

We use three environments:

1. **Development**: Local machine and server development environment
3. **Production**: What everyone sees

### AWS Credentials

In order for `zappa deploy` and other AWS command-line functions to work, you need to add your AWS credentials to a known location, usually somewhere like `~/.aws/credentials`. A sample `credentials` file would look something like this:

```
[app-name]
aws_access_key_id = some20characterstring
aws_secret_access_key = SomeOtherLonger40characterstring
```

### Zappa Settings

`profile_name`: Use the `app-name` that holds your AWS credentials

## Development

### Deployment

The first time, `zappa deploy development`

Thereafter, `zappa update development`

## Production

### AWS

1. Create a new AWS user to get security credentials. For permissions, add Lambda, API Gateway, RDS, IAM, and CloudFormation policies. At time of writing, `CloudFormation` requires a manual "inline" policy (as opposed to AWS-managed)
2. Create a public S3 bucket for your app to use for static assets
3. Create a PostgreSQL db. Your `DATABASE_URL` will be in the form `postgresql://user:pass@endpoint.rds.amazonaws.com/dbname`. If you plan to access the db remotely, use a dedicated security group and whitelist the IPs that you will use
4. Assign a VPC, subnets, and security group to your Lambda handler to enable proper permissions

### Static Assets

1. Upload Flask static assets with the `upload_assets.py` script, which should run automatically with no additional commands if the environment variables are set correctly
2. Navigate to your `.css` files and set the `Content-Type` metadata to `text/css`. Unfortunately this step must be done each time you upload, as there is no programmatic way to set the file metadata currently.

### Deployment

1. `zappa deploy production`
2. The first deployment requires extra steps. In addition to the environment variables passed via `zappa_settings.json`, navigate to your app's Lambda function and add the following variables:
    * `DATABASE_URL`
    * `SECRET_KEY`
    * `MAIL_USERNAME`
    * `MAIL_PASSWORD`
3. To update, `zappa update`
4. To view logs, `zappa tail --since 1h`

## Usage

### Database Migrations

0. Initialize: `flask db init`
1. Migrate: `flask db migrate`
2. Review code changes: `flask db edit`
3. Upgrade: `flask db upgrade`

### Static Assets

Custom css and js modules can be defined in `app/static/css/app.css` and `app/static/js/app.js` respectively. We already load in bulma, jquery, and fontawesome.

### Long Tasks

Lambda has a timeout of 30s, so longer-running tasks cannot be synchronously executed. To get around this, we asynchronously execute tasks with zappa's `@task` decorator. For an example, see the `email.py` function.

## References

* [explore flask](https://exploreflask.com/en/latest/index.html)
* [official flask](http://flask.pocoo.org/)
* [hack4impact/flask-base](https://github.com/hack4impact/flask-base)
