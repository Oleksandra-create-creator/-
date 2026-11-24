from flask import Flask, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')

with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username='admin'))
        db.session.add(Book(title='Python Crash Course', price=25.0))
        db.session.add(Book(title='Flask Web Development', price=30.0))
        db.session.commit()

@app.route('/')
def index():
    books = Book.query.all()
    html = '<h1>Онлайн-замовлення книг</h1>'
    if 'username' in session:
        html += f'<p>Вітаємо, {session["username"]}! <a href="/logout">Вихід</a></p>'
    else:
        html += '<p><a href="/login">Увійти</a></p>'
    for b in books:
        html += f'<p>{b.title} - {b.price} грн. <a href="/order/{b.id}">Замовити</a></p>'
    return html + '<br><a href="/api/books">REST API</a> | <a href="/orders">Мої замовлення</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '<form method="post"><input name="username" placeholder="Ім\'я" required><button>Увійти</button></form>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/order/<int:book_id>')
def order_book(book_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    book = Book.query.get_or_404(book_id)
    new_order = Order(user_id=user.id, book_id=book.id)
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/orders')
def view_orders():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(username=session['username']).first()
    html = '<h1>Мої замовлення</h1><a href="/">Назад</a><ul>'
    for o in user.orders:
        html += f'<li>{o.book.title} - {o.status}</li>'
    return html + '</ul>'

@app.route('/api/books', methods=['GET'])
def api_get_books():
    return jsonify([{'id': b.id, 'title': b.title, 'price': b.price} for b in Book.query.all()])

@app.route('/api/books', methods=['POST'])
def api_create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], price=data['price'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'id': new_book.id, 'title': new_book.title}), 201

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, port=5000)
