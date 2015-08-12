
from datetime import datetime
from registry.db import db
from registry.user.models import User
from registry.lib.index.db import Service

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comment = db.Column(db.UnicodeText)
    create_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    ip = db.Column(db.String(16), nullable=False)
    visible = db.Column(db.Boolean(), nullable=False, default=True)

    user = db.relationship(User, backref='comments', lazy='joined')
    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'))

    service = db.relation(Service, backref='comments', lazy='joined')
    service_id = db.Column(db.Integer, db.ForeignKey(Service.id, ondelete='CASCADE'))
