from flask import Flask, request, jsonify
from datetime import datetime
from functools import wraps

app = Flask(__name__)

class StudentSerializer:
    @staticmethod
    def serialize(student: dict, fields: list = None) -> dict:
        res = {}
        for k, v in student.items():
            if not fields or k in fields:
                res[k] = v.isoformat() if isinstance(v, datetime) else v
        return res

    @staticmethod
    def deserialize(data: dict) -> dict:
        if "name" not in data or "group" not in data:
            raise ValueError("name та group обов'язкові")
        return {"name": str(data["name"]), "group": str(data["group"]), "email": str(data.get("email", "")), "gpa": float(data.get("gpa", 0))}

    @staticmethod
    def serialize_list(students: list, fields: list = None) -> list:
        return [StudentSerializer.serialize(s, fields) for s in students]

@app.before_request
def log_request():
    print(f"[{datetime.now().isoformat()}] {request.method} {request.path}")

@app.after_request
def add_headers(response):
    response.headers["X-Request-Time"] = datetime.now().isoformat()
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-API-Key") != "secret-api-key-123":
            return jsonify({"error": "Невірний API-ключ"}), 401
        return f(*args, **kwargs)
    return wrapper

class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"error": error.message, "status": error.status_code, "details": error.details, "timestamp": datetime.now().isoformat()}), error.status_code

students_db = {}
next_id = 1

@app.route("/api/v2/students", methods=["GET"])
def get_students_v2():
    fields = request.args.get('fields', '').split(',') if request.args.get('fields') else None
    search = request.args.get('search', '').lower()
    sort_by = request.args.get('sort', 'name')
    order = request.args.get('order', 'asc')
    
    filtered = [s for s in students_db.values() if not search or search in s["name"].lower()]
    filtered.sort(key=lambda x: x[sort_by], reverse=(order == 'desc'))
    
    return jsonify({"students": StudentSerializer.serialize_list(filtered, fields)})

@app.route("/api/v2/students", methods=["POST"])
@require_api_key
def create_student_v2():
    global next_id
    try:
        data = StudentSerializer.deserialize(request.get_json())
    except ValueError as e:
        raise APIError(str(e), 422)
    
    student = {"id": next_id, **data, "created_at": datetime.now()}
    students_db[next_id] = student
    next_id += 1
    return jsonify(StudentSerializer.serialize(student)), 201

if __name__ == "__a__main__":
    app.run(debug=True, port=5006)
