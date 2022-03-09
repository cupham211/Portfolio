# Author: Christine Pham
# Date: Dec 4, 2021
from google.cloud import datastore
from flask import Flask, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import constants, bag, item, helpers
import requests
from urllib.request import urlopen
from jose import jwt
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.register_blueprint(bag.bp)
app.register_blueprint(item.bp)
app.register_blueprint(helpers.bp)

app.secret_key = constants.get_secret() 

client = datastore.Client()



oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=constants.CLIENT_ID,
    client_secret=constants.CLIENT_SECRET,
    api_base_url="https://" + constants.DOMAIN,
    access_token_url="https://" + constants.DOMAIN + "/oauth/token",
    authorize_url="https://" + constants.DOMAIN + "/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def index():
    # render auth0 welcome screen
    return auth0.authorize_redirect(redirect_uri= request.base_url + 'callback')

# Decode the JWT supplied in the Authorization header 
# ----FOR TESTING ONLY------------------------------------------------
#@cross_origin(headers=['Content-Type', 'Authorization'])
@app.route('/decode', methods=['GET'])
def decode_jwt():
    payload = helpers.verify_jwt(request)
    return payload 

@app.route('/callback')
def callback():
    # Handles response from token endpoint
    res = auth0.authorize_access_token()
    res_payload = auth0.get('userinfo')
    res_payload = res_payload.json()

    # store info into DATASTORE
    new_user = datastore.entity.Entity(key=client.key(constants.users))
    new_user.update({"username": res_payload['name'], "auth_id": res_payload['sub'], "bags": None})
    client.put(new_user)


    return render_template('dashboard.html', jwt=json.dumps(res, indent=4), name= res_payload["name"], \
        id=new_user.key.id)

@app.route('/users', methods=['GET', 'POST'])
def get_post_users():
    # check if accepted request is json
    if 'application/json' not in request.headers.get('Accept') and request.headers.get('Accept') != "*/*":
        res = {"Error":  "Requested a MIME type unsupported by endpoint"}
        return res, 406  

    if request.method == 'GET':
        query = client.query(kind=constants.users)
        results = list(query.fetch())
        # build response w empty dictionary
        res = {"users":[]}
        for e in results:
            res['users'].append(e.key.id)
        return res
# ---------------------------------FOR TESTING ONLY-------------------------------------------------
    elif request.method == 'POST':
        content = request.get_json()
        username = content["username"]
        password = content["password"]
        body = {'grant_type':'password','username':username,
            'password':password,
            'client_id':constants.CLIENT_ID,
            'client_secret':constants.CLIENT_SECRET
           }
        # exchange a grant code from auth0 for a JWT
        headers = { 'content-type': 'application/json' }
        url = 'https://' + constants.DOMAIN + '/oauth/token'
        # auth0 returns a JWT
        r = requests.post(url, json=body, headers=headers)

        # store info into DATASTORE
        new_user = datastore.entity.Entity(key=client.key(constants.users))
        new_user.update({"username": r['name'], "auth_id": r['sub'], "bags": None})
        client.put(new_user)

        return r.text, 201
    
    else:
        res = {"Error":  "Illegal request on root /users"}

        return res, 405


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)