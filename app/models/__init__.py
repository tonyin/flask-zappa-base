from app import db

class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=db.func.now())
    last_updated = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance is None:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
    return instance

from .user import *
from .model import *
