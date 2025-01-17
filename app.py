import os

from flask import (Flask, redirect, render_template, request, url_for)
import workos

# Flask Setup
DEBUG = False
app = Flask(__name__)

# WorkOS Setup

workos.api_key = os.getenv('WORKOS_API_KEY')
workos.project_id = os.getenv('WORKOS_PROJECT_ID')
workos.base_api_url = 'http://localhost:7000/' if DEBUG else workos.base_api_url

# There'd realistically be persons with different domains trying to sign in,
# where some may have SSO and some may not. This example assumes only workos.com
# domains with SSO setup.
CUSTOMER_EMAIL_DOMAIN = 'gmail.com'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/auth')
def auth():
    authorization_url = workos.client.sso.get_authorization_url(
        CUSTOMER_EMAIL_DOMAIN,
        url_for('auth_callback', _external=True),
        state={}
    )

    return redirect(authorization_url)

@app.route('/auth/callback')
def auth_callback():
    code = request.args.get('code')
    profile = workos.client.sso.get_profile(code)

    return profile.to_dict()
