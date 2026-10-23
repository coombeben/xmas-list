import random

from flask import Blueprint, request, abort

from app.extensions import db
from app.models import User, Item, Purchase

users_bp = Blueprint('users', __name__)

COLOURS = ['#9e0142', '#d53e4f', '#f4693e', '#e87502', '#bc8a01', '#869e10', '#869e10', '#41a485',
           '#3288bd', '#5e4fa2', '#7b3294', '#006d77', '#264653', '#3d405b', '#6a4c32', '#386641']


def new_colour() -> str:
    existing_colours = set(db.session.scalars(db.select(User.colour).distinct()).all())
    for colour in COLOURS:
        if colour not in existing_colours:
            return colour

    return random.choice(COLOURS)


@users_bp.route('', methods=['GET', 'POST'])
def handle_users():
    """Methods allowed:
        GET: Return all users
        POST: Create a new user
    """
    if request.method == 'GET':
        users = db.session.execute(db.select(User)).scalars()
        users_list = [user.to_dict() for user in users]
        return users_list, 200

    elif request.method == 'POST':
        content = request.get_json()
        name = content.get('name')
        colour = content.get('colour')

        if not name:
            abort(400)

        if not colour:
            colour = new_colour()

        user = User(name=name, colour=colour)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


@users_bp.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id: int):
    """Methods allowed:
        GET: Return a specific user
        PUT: Update a specific user
        DELETE: Delete a specific user
    """
    user = db.get_or_404(User, user_id)

    if request.method == 'GET':
        return user.to_dict(), 200

    elif request.method == 'PUT':
        content = request.get_json()
        for key, value in content.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user.to_dict(), 200

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {}, 204


@users_bp.route('/<int:user_id>/lists', methods=['GET'])
def get_others_lists(user_id: int):
    """Methods allowed:
        GET: Return a list of other user's lists
    """
    other_users = db.session.execute(
        db.select(User.user_id, User.name)
        .where(User.user_id != user_id)
        .order_by(User.user_id)
    ).fetchall()

    other_users_lists = []

    for other_user in other_users:
        other_user_id, other_user_name = other_user
        items_query = (
            db.select(
                Item.item_id,
                Item.name,
                Item.description,
                User.user_id,
                User.name.label('purchased_by'),
            )
            .outerjoin(Purchase, Purchase.item_id == Item.item_id)
            .outerjoin(User, User.user_id == Purchase.user_id)
            .where(Item.user_id == other_user_id)
            .order_by(Item.item_id)
        )
        items_result = db.session.execute(items_query).fetchall()

        items = []
        for item in items_result:
            item_id, item_name, item_description, user_id, purchased_by = item
            items.append({
                'item_id': item_id,
                'name': item_name,
                'description': item_description,
                'purchased_by_user_id': user_id,
                'purchased_by': purchased_by
            })

        other_users_lists.append({
            'user_id': other_user_id,
            'username': other_user_name,
            'items': items
        })

    return other_users_lists, 200
