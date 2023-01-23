# -*- coding: utf-8 -*-

import os
import requests
import re
import json

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import flask
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_cors import CORS


DEBUG = True


# Configuration
CLIENT_SECRETS_FILE = "secret/client_secret.json"
with open(CLIENT_SECRETS_FILE) as f:
  _CLIENT_SECRETS_JSON = json.load(f)
GOOGLE_CLIENT_ID = _CLIENT_SECRETS_JSON['web']['client_id']
GOOGLE_CLIENT_SECRET = _CLIENT_SECRETS_JSON['web']['client_secret']
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/drive.metadata"]
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'


# Flask app setup
app = flask.Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
CORS(app, resources=r'https://192.168.1.93:5443/*')


SERVER_NAME = 'www.homeautomationapi.tk'
url_pat = 'https?://[a-z0-9,.]*/'


def check_credentials():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return True


@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return flask.render_template('index.html')


@app.route('/authorize')
def authorize():
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = "https://www.homeautomationapi.tk/oauth2callback"

  if DEBUG:
    print("######### @app.route('/authorize') ################")
    print(f"[DEBUG] flow: {flow}")
    print(f"[DEBUG] flask.request.environ: {flask.request.environ}")
    print(f"[DEBUG] {flow.redirect_uri}")
 
  authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')
 
  # Store the state so the callback can verify the auth server response.
  flask.session['state'] = state
 
  return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verified in the authorization server response.
  state = flask.session['state']

  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  # flow.redirect_uri = flask.url_for('oauth2callback', _external=True)
  flow.redirect_uri = "https://www.homeautomationapi.tk/oauth2callback"

  if DEBUG:
    print("######### @app.route('/oauth2callback') ################")
    print(f"[DEBUG] flow.redirect_uri: {flow.redirect_uri}")

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  if "http:" in authorization_response:
    authorization_response = authorization_response.replace("http:","https:") 
  if DEBUG:
    print(f"[DEBUG] authorization_response: {authorization_response}")

  flow.fetch_token(authorization_response=authorization_response)

  # Store credentials in the session.
  # ACTION ITEM: In a production app, you likely want to save these
  #              credentials in a persistent database instead.
  credentials = flow.credentials
  flask.session['credentials'] = credentials_to_dict(credentials)

  return flask.redirect("https://www.homeautomationapi.tk/")


@app.route('/revoke')
def revoke():
  if 'credentials' not in flask.session:
    return ('You need to <a href="/authorize">authorize</a> before ' +
            'testing the code to revoke credentials.')

  credentials = google.oauth2.credentials.Credentials(
    **flask.session['credentials'])

  revoke = requests.post('https://oauth2.googleapis.com/revoke',
      params={'token': credentials.token},
      headers = {'content-type': 'application/x-www-form-urlencoded'})

  status_code = getattr(revoke, 'status_code')
  if status_code == 200:
    return('Credentials successfully revoked.' + print_index_table())
  else:
    return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
  if 'credentials' in flask.session:
    del flask.session['credentials']
  return ('Credentials have been cleared.<br><br>' +
          print_index_table())


@app.route('/api', methods=['POST', 'GET'])
def api():
  dir(flask.request)
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  api_end = flask.request.args.get('api')
  api_com = flask.request.args.get('command')
  if api_end:
    print(f"[DEBUG] api_end: {api_end}")
    if api_com:
      print(f"[DEBUG] api_com: {api_com}")      
      resp = requests.get(url=f"http://192.168.1.93:5000/{api_com}")
      print(f"[DEBUG] resp: {resp}")
    return ({"api_end": api_end, "api_com": api_com})
  
  return flask.render_template('api.html')


@app.route('/api/desklamp/power', methods=['GET'])
def api_desklamp_power():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return("/api/desklamp/power")


@app.route('/api/desklamp/hue', methods=['GET'])
def api_desklamp_hue():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return("/api/desklamp/hue")


@app.route('/api/desklamp/brighter', methods=['GET'])
def api_desklamp_brighter():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return("/api/desklamp/brighter")


@app.route('/api/desklamp/dimmer', methods=['GET'])
def api_desklamp_dimmer():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return("/api/desklamp/dimmer")


@app.route('/contact', methods=['GET'])
def contact():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return flask.render_template('contact.html')


@app.route('/about', methods=['GET'])
def about():
  if 'credentials' not in flask.session:
    return flask.redirect("https://www.homeautomationapi.tk/authorize")
  return flask.render_template('about.html')


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification.
  # ACTION ITEM for developers:
  #     When running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  # Specify a hostname and port that are set as a valid redirect URI
  # for your API project in the Google API Console.
  app.run('127.0.0.1', 5000, debug=True, ssl_context=("C:\certs\certificate.pem", "C:\certs\key.pem"))