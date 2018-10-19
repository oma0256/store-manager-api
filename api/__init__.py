"""
Set up flask
"""

from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'super secret key'


@app.before_first_request
def clear_session():
    """
    Clear session whenever server restarts
    """
    session.clear()

from api import views
