import os
import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request
from sqlalchemy import text

from app.extensions import db
from app.models import Session

auth_bp = Blueprint('auth', __name__)


def validate_token(token: str) -> bool:
    token = token.replace('Bearer ', '')
    session = db.session.get(Session, token)
    if not session:
        return False

    return (datetime.now() - session.created) < timedelta(days=7)


@auth_bp.route('/authenticate', methods=['POST'])
def authenticate():
    content = request.get_json()
    password = content.get('password', '')

    if password != os.environ.get('APP_PASSWORD'):
        return {'success': False}, 401

    token = secrets.token_urlsafe(32)
    session = Session(token=token)
    db.session.add(session)
    db.session.commit()
    return {'success': True, 'token': token}, 200


@auth_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    db.session.execute(text('SELECT 1'))
    return {'status': 'ok'}
