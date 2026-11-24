from flask import Flask, request, make_response, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = "super-secret-key"

@app.route("/set-theme/<theme>")
def set_theme(theme):
    resp = make_response("Theme set")
    resp.set_cookie('theme', theme, max_age=60*60*24*30, httponly=True, samesite='Lax')
    return resp

@app.route("/get-theme")
def get_theme():
    return jsonify({"theme": request.cookies.get('theme', 'light')})

@app.route("/set-language/<lang>")
def set_language(lang):
    resp = make_response("Language set")
    resp.set_cookie('language', lang)
    return resp

@app.route("/preferences")
def preferences():
    return jsonify({"cookies": request.cookies})

@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return jsonify({"cart": session['cart']})

@app.route("/cart")
def view_cart():
    return jsonify({"cart": session.get('cart', [])})

@app.route("/cart/clear")
def clear_cart():
    session.pop('cart', None)
    return jsonify({"message": "Cart cleared"})

@app.route("/login", methods=["POST"])
def login():
    session['username'] = request.form.get('username', 'Guest')
    return redirect(url_for('profile'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('profile'))

@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    return jsonify({"user": session['username']})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
