from flask import Flask, request, render_template_string, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "blog-secret-key"

DELETE_CONFIRM_TEMPLATE = """<!DOCTYPE html><html><body><h1>Видалення</h1>
<p>Видалити "<strong>{{ post.title }}</strong>"?</p>
<form method="POST"><button type="submit" style="color:red">Так</button> <a href="{{ url_for('post_detail', post_id=post.id) }}">Скасувати</a></form></body></html>"""

FORM_TEMPLATE = """<!DOCTYPE html><html><body><h1>Редагування</h1>
<form method="POST"><input type="text" name="title" value="{{ post.title }}" required><br>
<input type="text" name="author" value="{{ post.author }}" required><br>
<textarea name="content" required>{{ post.content }}</textarea><br>
<button type="submit">Зберегти</button> <a href="{{ url_for('post_list') }}">Скасувати</a></form></body></html>"""

posts_db = [{"id": 1, "title": "Перша", "content": "Зміст", "author": "Іван", "created_at": "2025-01-15"}]
next_id = 2

@app.route("/posts")
def post_list():
    return f"<h1>Список</h1>" + "".join([f"<a href='/posts/{p['id']}'>{p['title']}</a><br>" for p in posts_db])

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post: abort(404)
    return f"<h1>{post['title']}</h1><p>{post['content']}</p><a href='{url_for('post_edit', post_id=post_id)}'>Редагувати</a> | <a href='{url_for('post_delete', post_id=post_id)}'>Видалити</a> | <a href='/posts'>Назад</a>"

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def post_edit(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post: abort(404)
    if request.method == "POST":
        post.update({"title": request.form["title"], "content": request.form["content"], "author": request.form["author"]})
        flash("Оновлено!")
        return redirect(url_for("post_detail", post_id=post_id))
    return render_template_string(FORM_TEMPLATE, post=post)

@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def post_delete(post_id):
    post = next((p for p in posts_db if p["id"] == post_id), None)
    if not post: abort(404)
    if request.method == "POST":
        posts_db.remove(post)
        flash("Видалено!")
        return redirect(url_for("post_list"))
    return render_template_string(DELETE_CONFIRM_TEMPLATE, post=post)

if __name__ == "__main__":
    app.run(debug=True, port=5004)
