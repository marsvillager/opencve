from sqlalchemy.dialects.postgresql import JSONB
from flask_user import current_user
from sqlalchemy_utils import UUIDType
from opencve.extensions import db
import uuid


def get_uuid():
    return str(uuid.uuid4())


class Endpoint(db.Model):

    __table_args__ = {'extend_existing': True}
    __tablename__ = "endpoints"

    id = db.Column(
        UUIDType(binary=False), primary_key=True, nullable=False, default=get_uuid
    )
    mac = db.Column(db.String(), unique=True, nullable=True)
    json = db.Column(JSONB, nullable=True)

    def __repr__(self):
        return '<Endpoint %r>' % self.id