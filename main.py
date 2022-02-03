from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib
import os


MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PW = os.environ.get("MY_PW")

app = Flask(__name__)

# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///subscriber.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f'<User {self.title}>'

db.create_all()



@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        if request.form['form'] == 'contact_btn':
            name = request.form['contactName']
            email = request.form['contactEmail']
            subject = request.form['contactSubject']
            message = request.form['contactMessage']

            new_email = Subscriber(db_email=email)
            db.session.add(new_email)
            db.session.commit()

            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PW)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs="hello@5deeptech.com",
                    msg=f"SENT FROM 5DEEPTECH.COM\n\nSubject:{subject}\nName: {name}\nEmail: {email}\nMessage: {message}"
                )

        elif request.form['form'] == 'subscribe_btn':
            email = request.form['Email']
            new_email = Subscriber(
                db_email=email
            )
            db.session.add(new_email)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)