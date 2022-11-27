import json
from flask import Flask, render_template, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

import google.oauth2.credentials
import google_auth_oauthlib.flow


# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'secret/client_secret.json',
    scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = 'https://www.example.com/oauth2callback'

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')



app = Flask(__name__)
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api')
def api():
    with open("/Users/tomotero/Projects/web/HomeAutomationAPI/api_note", "a") as f:
        f.write("HERE!")
    return ("<p>API ENDPOINT!</p>")

def main(environ, start_response):
    app.run(host='127.0.0.1', port=8080, debug=True)

if __name__ == "__main__":
    main()