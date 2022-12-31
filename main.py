from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired, Length
import smtplib
import os


# SETUP THE FLASK APP
app = Flask(__name__)
Bootstrap(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Email Credentials
my_email = "merkamkiris@gmail.com"
my_password = "tizpomprqsllqayv"


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email_address = EmailField("Email Address", validators=[DataRequired()])
    phone_number = IntegerField("Phone Number")
    message = StringField("Message", validators=[DataRequired(), Length(1, 400)])
    submit = SubmitField('Send')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/portfolio")
def portfolio_page():
    return render_template("portfolio.html")


@app.route("/contact-me", methods=["GET", "POST"])
def contact_page():
    form = ContactForm()
    name = form.name.data
    message = form.message.data
    phone = form.phone_number.data
    email = form.email_address.data
    submit = form.submit.data
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="erkamkiris@gmail.com",
                msg=f"Subject:{form.name.data} Wants to Contact You!"
                    f"\n\nName:{form.name.data}"
                    f"\n\nMessage:{form.message.data}"
                    f"\n\n Phone Number: {form.phone_number.data}"
                    f" \n\n Email Address: {form.email_address.data}"
            )
        return redirect(url_for("home"))
    return render_template("contact.html", form=form, name=name, email=email, message=message, phone=phone, submit=submit)


@app.route("/about")
def about_me_page():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
