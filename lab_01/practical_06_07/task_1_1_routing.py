from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

BASE_TEMPLATE = """<!DOCTYPE html><html><head><title>{{ title }}</title></head>
<body><h1>{{ title }}</h1><nav><a href="{{ url_for('index') }}">Головна</a> | 
<a href="{{ url_for('post_list') }}">Публікації</a> | <a href="{{ url_for('search') }}">Пошук</a></nav><hr>{{ content | safe }}</body></html>"""

posts_db = [{"id": 1, "title": "Вступ до Python", "content": "Python...", "author": "Іван"}]
next_id = 2

@app.route("/")
def index():
    return render_template_string(BASE_TEMPLATE, title="Головна", content="<p>Ласкаво просимо!</p>")

@app.route("/posts")
def post_list():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    return render_template_string(BASE_TEMPLATE, title="Публікації", content=str(posts_db[start:start+per_page]))

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        return "404 Not Found", 404
    return render_template_string(BASE_TEMPLATE, title=post["title"], content=f"<p>{post['content']}</p><p>Автор: {post['author']}</p>")

@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id
    if request.method == "POST":
        posts_db.append({"id": next_id, "title": request.form["title"], "content": request.form["content"], "author": request.form["author"]})
        next_id += 1
        return redirect(url_for("post_list"))
    return render_template_string(BASE_TEMPLATE, title="Створити", content='<form method="POST"><input name="title" required><input name="author" required><textarea name="content" required></textarea><button>Створити</button></form>')

@app.route("/search")
def search():
    q = request.args.get('q', '')
    return render_template_string(BASE_TEMPLATE, title="Пошук", content=f"Результати для: {q}")

@app.route("/archive/<int:year>/<int:month>")
def archive(year, month):
    return render_template_string(BASE_TEMPLATE, title="Архів", content=f"Архів за {year}-{month:02d}")

@app.route("/user/<username>")
def user_profile(username):
    return render_template_string(BASE_TEMPLATE, title="Профіль", content=f"Користувач: {username}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
