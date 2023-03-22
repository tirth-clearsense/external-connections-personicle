from .base import db
from datetime import datetime

# SQLAlchemy models
class ExternalConnections(db.Model):
    """
    Fields
    required:
    personicle_user_id: User id for the user in personicle servers
    service_name: Name of the external service
    access_token: Access token value
    expires_in: Time before expiration for the token
    created_at: Time of token creation

    Optional arguments:
    external_user_id: user id for the external API service (e.g. fitbit user id)
    refresh_token: Refresh token value
    """
    # __tablename__ = "usertokens"

    # required fields
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(50), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    access_token = db.Column(db.String(500), nullable=False)
    expires_in = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # optional fields
    external_user_id = db.Column(db.String(50))
    refresh_token = db.Column(db.String(500))
    status = db.Column(db.String(500))
    # usage fields
    last_accessed_at = db.Column(db.DateTime, nullable=True)
    scope=db.Column(db.String(500), nullable=True)

    def __repr__(self) -> str:
        return f"UserToken('{self.userId}', '{self.service}', '{self.expires_in}', '{self.created_at}')"

