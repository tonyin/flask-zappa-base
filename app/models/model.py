from .. import db
from . import TimestampMixin


class Example(TimestampMixin, db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
