from flask import Flask, request, render_template_string, redirect, url_for, flash, abort
from datetime import datetime

app = Flask(__name__)
app.secret_key = "blog-secret-key"

LIST_TEMPLATE = """<!DOCTYPE html><html><body><h1>Блог</h1>
{% with messages = get_flashed_messages() %}{% if messages %}<p style="color:green">{{ messages[0] }}</p>{% endif %}{% endwith %}
<a href="{{ url_for('post_create') }}">+ Нова</a><hr>
{% for post in posts %}<h2><a href="{{ url_for('post_detail', post_id=post.id) }}">{{ post.title }}</a></h2>
<p>{{ post.content[:100] }}...</p><small>{{ post.author }} | {{ post.created_at }}</small><hr>{% endfor %}</body></html>"""

FORM_TEMPLATE = """<!DOCTYPE html><html><body><h1>{{ form_title }}</h1>
<form method="POST"><label>Заголовок:</label><br><input type="text" name="title" value="{{ post.title if post else '' }}" required><br><br>
<label>Автор:</label><br><input type="text" name="author" value="{{ post.author if post else '' }}" required><br><br>
<label>Зміст:</label><br><textarea name="content" rows="5" required>{{ post.content if post else '' }}</textarea><br><br>
<button type="submit">{{ button_text }}</button> <a href="{{ url_for('post_list') }}">Скасувати</a></form></body></html>"""

posts_db = []
next_id = 1

@app.route("/posts")
def post_list():
    page = int(request.args.get('page', 1))
    per_page = 2
    start = (page - 1) * per_page
    return render_template_string(LIST_TEMPLATE, posts=posts_db[start:start+per_page])

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post:
        abort(404)
    return f"<h1>{post['title']}</h1><p>{post['content']}</p><a href='{url_for('post_list')}'>Назад</a>"

@app.route("/posts/create", methods=["GET", "POST"])
def post_create():
    global next_id
    if request.method == "POST":
        if not request.form["title"] or not request.form["content"]:
            flash("Заповніть всі поля")
            return redirect(url_for("post_create"))
        posts_db.append({"id": next_id, "title": request.form["title"], "content": request.form["content"], "author": request.form["author"], "created_at": datetime.now().strftime("%Y-%m-%d")})
        next_id += 1
        flash("Публікацію створено!")
        return redirect(url_for("post_list"))
    return render_template_string(FORM_TEMPLATE, form_title="Нова публікація", button_text="Створити", post=None)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
