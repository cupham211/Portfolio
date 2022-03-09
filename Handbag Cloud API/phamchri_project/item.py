# Author: Christine Pham
# Date: Dec 4, 2021
from flask import Blueprint, request, jsonify, make_response
from datetime import datetime
from google.cloud import datastore
import urllib.parse
import constants, helpers
import requests
from jose import jwt
import json
from helpers import verify_jwt
from os import environ as env
from werkzeug.exceptions import HTTPException

client = datastore.Client()

bp = Blueprint('item', __name__, url_prefix='/items')

# Create a item or view all items
@bp.route('', methods=['POST','GET'])
def items_get_post():
    # check if accepted request is json
    if 'application/json' not in request.headers.get('Accept') and request.headers.get('Accept') != "*/*":
        res = {"Error":  "Requested a MIME type unsupported by endpoint"}
        return res, 406  

    if request.method == 'POST':
        content = request.get_json()
        if "name" not in content or "category" not in content:
            res = {
                "Error": "The request object is missing at least one required attribute"
            }
            return res, 400
        new_item = datastore.entity.Entity(key=client.key(constants.items))
        # create create date string
        date = datetime.now()
        new_item.update({"name": content["name"], "carrier": None, "category": content["category"],
            "creation_date": date.strftime("%m/%d/%Y")})
        client.put(new_item)
        # build res obj
        new_item["id"] = new_item.key.id
        new_item["self"] = str(request.base_url) + '/' + str(new_item.key.id)
        return new_item, 201

    # View all items with pagination
    elif request.method == 'GET':
        cursor = request.args.get('cursor', default = None, type = str)
        query = client.query(kind=constants.items)
        query_iter = query.fetch(start_cursor=cursor, limit=5)
        page = next(query_iter.pages)
        # objects displayed for current page
        cur_results = list(page)
        if query_iter.next_page_token:
            next_url = str(request.base_url) + "?cursor=" + urllib.parse.quote(query_iter.next_page_token)
        else:
            next_url = None
        # populate display for each object on current page
        for e in cur_results:
            e["id"] = e.key.id
            e["self"] = str(request.base_url) + '/' + str(e.key.id)
            # append self link to obj in carrier
            if e["carrier"]:
                e["carrier"]["self"] = str(request.url_root) + 'bags/' + str(e["carrier"]["id"])
        # build res object
        res = {"count": len(list(query.fetch()))}
        res["items"] = cur_results
        if next_url:
            res["next"] = next_url
        return res
    else:
        res = {"Error":  "Illegal request on root /items"}

        return res, 405

# View a item or delete a item
@bp.route('/<id>', methods=['GET','PUT', 'PATCH', 'DELETE'])
def items_get_delete(id):
    item_key = client.key(constants.items, int(id))
    item = client.get(key=item_key)

    if not item:
        res = {"Error": "The specified item does not exist"}
        return res, 404

    if request.method == 'GET':
        # check if accepted request is json
        if 'application/json' not in request.headers.get('Accept') and request.headers.get('Accept') != "*/*":
            res = {"Error":  "Requested a MIME type unsupported by endpoint"}
            return res, 406 
        item["id"] = item.key.id
        # if item is in a bag create a link
        if item["carrier"]:
            item["carrier"]["self"] = str(request.url_root) + 'bags/' + str(item["carrier"]["id"])
        item["self"] = str(request.base_url)
        return jsonify(item)

    # deletes an item and updates the bag if item was in a bag
    # items inside bags require a token
    elif request.method == 'DELETE':
        # if item has a carrier but not token
        if item["carrier"] and 'Authorization' not in request.headers:
            res = {"Error":  "Valid tokens needed to delete items inside bags"}
            return res, 403
        # remove item from bag that is carrying it
        if item["carrier"] and 'Authorization' in request.headers:
            # verify jot FIRST---------------------------------------------------401
            payload = verify_jwt(request)
            bag_key = client.key(constants.bags, int(item["carrier"]["id"]))
            bag = client.get(key=bag_key)
            # get the user object from bag['owner']
            user_key = client.key(constants.users, int(bag['owner']))
            user = client.get(key=user_key)
            if user['auth_id'] != payload['sub']:
                res = {"Error":  "user token and ID don’t match"}
                return res, 403

            # remove item from bag first if inside bag
            bag["items"].remove(item.key.id)
            if not bag["items"]:
                bag.update({"items": None})
            client.put(bag)

        client.delete(item_key)
        return ('',204)
    elif request.method == 'PUT' or request.method == 'PATCH':
        # convert json to a dictionary
        content = request.get_json()
        if 'name' in content:
            item.update({"name": content["name"]})
        if 'category' in content:
            item.update({'category': content['category']})
        client.put(item)
        return ('', 204)
        
    else:
        res = {"Error":  "Illegal request on root /items"}

        return res, 405