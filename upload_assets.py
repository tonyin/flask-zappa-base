#!/usr/bin/env python3

import os
import flask_s3

from app import create_app

FLASKS3_FORCE_MIMETYPE = True
app = create_app('production')
flask_s3.create_all(
    app,
    os.getenv('AWS_ACCESS_KEY_ID'),
    os.getenv('AWS_SECRET_ACCESS_KEY')
)
print("Uploaded.")
