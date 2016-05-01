from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load default config
app.config.from_object('config')

# Load config from instance
app.config.from_pyfile('config.py')
