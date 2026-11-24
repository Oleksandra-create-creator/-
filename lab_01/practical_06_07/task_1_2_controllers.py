from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(silent=True)
            if data is None:
                return jsonify({"error": "Очікується JSON"}), 400
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({"error": f"Відсутні поля: {', '.join(missing)}"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

items_db = {1: {"id": 1, "name": "Ноутбук", "price": 25000, "category": "електроніка"}}
next_id = 2

@app.route("/api/items", methods=["GET"])
def get_items():
    category = request.args.get('category')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', float('inf')))
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    
    filtered = [i for i in items_db.values() if (not category or i['category'] == category) and min_price <= i['price'] <= max_price]
    filtered.sort(key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return jsonify({"count": len(filtered), "items": filtered})

@app.route("/api/items", methods=["POST"])
@validate_json(["name", "price", "category"])
def create_item():
    global next_id
    data = request.get_json()
    if not data["name"] or data["price"] <= 0:
        return jsonify({"error": "Некоректні дані"}), 400
    item = {"id": next_id, "name": data["name"], "price": data["price"], "category": data["category"]}
    items_db[next_id] = item
    next_id += 1
    return jsonify(item), 201

@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if item_id not in items_db:
        return jsonify({"error": "Не знайдено"}), 404
    return jsonify(items_db[item_id])

@app.route("/api/items/<int:item_id>", methods=["PUT"])
@validate_json(["name", "price", "category"])
def update_item(item_id):
    if item_id not in items_db:
        return jsonify({"error": "Не знайдено"}), 404
    data = request.get_json()
    items_db[item_id].update({"name": data["name"], "price": data["price"], "category": data["category"]})
    return jsonify(items_db[item_id])

@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id in items_db:
        del items_db[item_id]
    return "", 204

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)
