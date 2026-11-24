from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

students_db = {}
next_id = 1

@app.route("/api/students", methods=["GET"])
def get_students():
    group = request.args.get('group')
    min_gpa = float(request.args.get('min_gpa', 0))
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    filtered = [s for s in students_db.values() if (not group or s['group'] == group) and s['gpa'] >= min_gpa]
    filtered.sort(key=lambda x: x[sort_by], reverse=(order == 'desc'))
    
    start = (page - 1) * per_page
    return jsonify({"count": len(filtered), "page": page, "per_page": per_page, "students": filtered[start:start+per_page]})

@app.route("/api/students", methods=["POST"])
def create_student():
    global next_id
    data = request.get_json()
    if not data or not data.get("name") or not data.get("group"):
        return jsonify({"error": "name та group обов'язкові"}), 400
    if not (0 <= data.get("gpa", 0) <= 100):
        return jsonify({"error": "gpa має бути 0-100"}), 400
    if any(s["email"] == data["email"] for s in students_db.values() if s.get("email")):
        return jsonify({"error": "Email вже існує"}), 400
        
    student = {"id": next_id, "name": data["name"], "group": data["group"], "email": data.get("email", ""), "gpa": float(data.get("gpa", 0)), "created_at": datetime.now().isoformat()}
    students_db[next_id] = student
    next_id += 1
    return jsonify(student), 201

@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    if student_id not in students_db:
        return jsonify({"error": "Не знайдено"}), 404
    return jsonify(students_db[student_id])

@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    if student_id not in students_db:
        return jsonify({"error": "Не знайдено"}), 404
    data = request.get_json()
    students_db[student_id].update({"name": data["name"], "group": data["group"], "email": data["email"], "gpa": float(data["gpa"])})
    return jsonify(students_db[student_id])

@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    if student_id not in students_db:
        return jsonify({"error": "Не знайдено"}), 404
    data = request.get_json()
    if "gpa" in data:
        data["gpa"] = float(data["gpa"])
    students_db[student_id].update(data)
    return jsonify(students_db[student_id])

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    if student_id in students_db:
        del students_db[student_id]
    return "", 204

@app.route("/api/students/stats", methods=["GET"])
def students_stats():
    if not students_db:
        return jsonify({"total": 0, "avg_gpa": 0})
    gpas = [s["gpa"] for s in students_db.values()]
    groups = {}
    for s in students_db.values():
        groups[s["group"]] = groups.get(s["group"], 0) + 1
    return jsonify({"total": len(students_db), "avg_gpa": sum(gpas)/len(gpas), "groups": groups, "top_students": [s["name"] for s in students_db.values() if s["gpa"] >= 90]})

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ресурс не знайдено", "status": 404}), 404

if __name__ == "__main__":
    test_students = [{"name": "Іваненко О.", "group": "КІ-21", "email": "ivan@kpi.ua", "gpa": 85.5}, {"name": "Петренко М.", "group": "КІ-21", "email": "petro@kpi.ua", "gpa": 92.0}]
    for s in test_students:
        students_db[next_id] = {**s, "id": next_id, "created_at": datetime.now().isoformat()}
        next_id += 1
    app.run(debug=True, port=5005)
