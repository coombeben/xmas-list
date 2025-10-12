from flask import Blueprint, request, abort

from app.extensions import db
from app.models import Item, Purchase

items_bp = Blueprint('items', __name__)


@items_bp.route('', methods=['GET', 'POST'])
def handle_items(user_id: int):
    """Methods allowed:
        GET: Get all items for a given user
        POST: Create a new item
    """
    if request.method == 'GET':
        items = db.session.execute(
            db.select(Item)
            .filter_by(user_id=user_id)
            .order_by(Item.item_id)
        ).scalars()

        if not items:
            abort(404)

        items_list = [item.to_dict() for item in items]
        return items_list, 200

    elif request.method == 'POST':
        content = request.get_json()
        item = Item(user_id=user_id, **content)
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), 201


@items_bp.route('/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(user_id: int, item_id: int):
    """Methods allowed:
        GET: Get details of specific item
        PUT: Update specific item
        DELETE: Delete specific item
    """
    item = db.get_or_404(Item, item_id)
    if item.user_id != user_id:
        abort(403)

    if request.method == 'GET':
        return item.to_dict(), 200

    elif request.method == 'PUT':
        content = request.get_json()
        for key, value in content.items():
            if hasattr(item, key):
                setattr(item, key, value)
        db.session.commit()
        return item.to_dict(), 201

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return {}, 204


@items_bp.route('/<int:item_id>/purchase', methods=['POST', 'DELETE'])
def purchase_item(user_id: int, item_id: int):
    """Methods allowed:
        POST: Mark an item as purchased by the user
        DELETE: Unmark an item as purchased by the user
    """
    item = db.get_or_404(Item, item_id)
    if item.user_id == user_id:
        abort(403)

    if request.method == 'POST':
        purchase = Purchase(user_id=user_id, item_id=item_id)
        db.session.add(purchase)
        db.session.commit()
        return purchase.to_dict(), 201

    elif request.method == 'DELETE':
        purchase = db.session.execute(
            db.select(Purchase)
            .filter_by(user_id=user_id, item_id=item_id)
        ).scalar_one_or_none()
        db.session.delete(purchase)
        db.session.commit()
        return {}, 204
