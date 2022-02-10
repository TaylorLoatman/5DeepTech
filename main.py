from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.message import EmailMessage
import os


MY_PW = os.environ.get('MY_PW')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

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

            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = 'Web Service Inquiry'
            msg['To'] = 'hello@5deeptech.com'
            msg.set_content(f'{name}: {email}\n\n{message}')

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('tloatman3@gmail.com', MY_PW)
            server.send_message(msg)
            server.quit()


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