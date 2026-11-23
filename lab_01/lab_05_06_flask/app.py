from flask import Flask, render_template, redirect, url_for, flash
from forms import EventRegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-flask-key-for-lab'

@app.route('/')
def index():
    context = {
        'page_title': 'Головна сторінка',
        'event_name': 'Конференція Python розробників 2024',
        'attendees_count': 150,
        'speakers': ['Олена Петренко', 'Іван Мельник', 'Марія Коваль'],
    }
    return render_template('index.html', **context)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = EventRegistrationForm()
    if form.validate_on_submit():
        flash(f'Дякуємо, {form.name.data}! Вашу реєстрацію успішно прийнято.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
