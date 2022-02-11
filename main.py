from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Configure Mail
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'tloatman77@yahoo.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MY_PW')
mail = Mail(app)


# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL1', 'sqlite:///subscriber.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'<User {self.title}>'

# db.create_all()


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    error = None

    if request.method == 'POST':
        if request.form['form'] == 'contact_btn':
            name = request.form['contactName']
            email = request.form['contactEmail']
            subject = request.form['contactSubject']
            message = request.form['contactMessage']

            existing_email = Subscriber.query.filter_by(db_email=email).first()

            if existing_email:
                pass
            else:
                new_email = Subscriber(db_email=email)
                db.session.add(new_email)
                db.session.commit()

            msg = Message(subject=subject, sender='tloatman77@yahoo.com', recipients=['hello@5deeptech.com'])
            msg.body = f'From: {name}, {email}\n\n{message}'
            mail.send(msg)
            return redirect(url_for('home'))

        elif request.form['form'] == 'subscribe_btn':
            email = request.form['Email']
            existing_email = Subscriber.query.filter_by(db_email=email).first()
            if existing_email:
                pass
            else:
                new_email = Subscriber(
                    db_email=email
                )
                db.session.add(new_email)
                db.session.commit()
                return redirect(url_for('home'))

    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
