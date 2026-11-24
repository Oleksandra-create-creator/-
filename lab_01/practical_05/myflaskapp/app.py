from flask import Flask, jsonify, request
from config import config_by_name

def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    register_routes(app)
    return app

def register_routes(app: Flask):
    @app.route('/')
    def index():
        return "<h1>Ласкаво просимо до Flask!</h1><p><a href='/about'>Про проєкт</a> | <a href='/api/info'>API Info</a></p>"

    @app.route('/about')
    def about():
        return "<h1>Про Flask-додаток</h1><p>Це мінімальний проєкт з патерном Application Factory.</p>"

    @app.route('/api/info')
    def api_info():
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        return jsonify({
            "framework": "Flask",
            "version": "3.0.0",
            "debug": app.config.get('DEBUG'),
            "routes": routes
        })

    @app.route('/greet', defaults={'name': None})
    @app.route('/greet/<name>')
    def greet(name):
        display_name = name or request.args.get('name', 'Гість')
        return f"<h1>Привіт, {display_name}!</h1>"

if __name__ == '__main__':
    application = create_app('development')
    application.run(debug=True, port=5000)
