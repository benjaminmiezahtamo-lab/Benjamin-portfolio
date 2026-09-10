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


import resend
import os

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    try:
        resend.api_key = os.getenv("RESEND_API_KEY")

        resend.Emails.send({
            "from": "Portfolio <onboarding@resend.dev>",
            "to": [os.getenv("MAIL_USERNAME")],
            "subject": f"Portfolio Contact: {name}",
            "reply_to": email,
            "text": f"""
You received a new message from your portfolio.

Name: {name}
Email: {email}

Message:
{message}
"""
        })

        return "Message sent successfully!", 200

    except Exception as e:
        print(f"Email error: {e}")
        return "Sorry, your message could not be sent. Please try again later.", 500


if __name__ == "__main__":
    app.run(debug=True)