from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    msg = EmailMessage()

    msg["Subject"] = f"Portfolio Contact: {name}"
    msg["From"] = os.getenv("MAIL_USERNAME")
    msg["To"] = os.getenv("MAIL_USERNAME")
    msg["Reply-To"] = email

    msg.set_content(
        f"""
You received a new message from your portfolio.

Name: {name}
Email: {email}

Message:
{message}
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("MAIL_USERNAME"),
            os.getenv("MAIL_PASSWORD")
        )
        smtp.send_message(msg)

    return "Message sent successfully!"


if __name__ == "__main__":
    app.run(debug=True)