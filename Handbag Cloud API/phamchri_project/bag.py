# Author: Christine Pham
# Dec 2, 2021

from flask import Blueprint, request, jsonify, make_response
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

bp = Blueprint('bag', __name__, url_prefix='/bags')

# Create a bag or view all bags
@bp.route('', methods=['POST','GET'])
def bags_get_post():
    # check if accepted request is json
    if 'application/json' not in request.headers.get('Accept') and request.headers.get('Accept') != "*/*":
        res = {"Error":  "Requested a MIME type unsupported by endpoint"}
        return res, 406   

    if request.method == 'POST':     
        # converts the json to a dictionary
        content = request.get_json()
        if "model" not in content or "brand" not in content:
            res = {
                "Error": "The request object is missing at least one of the required attributes"
                }
            return res, 400
        new_bag = datastore.entity.Entity(key=client.key(constants.bags))
        new_bag.update({"model": content["model"], "brand": content["brand"],
          "private": False, "owner": None, "items": None})
        client.put(new_bag)
        res = new_bag
        res["id"] = new_bag.key.id
        res["self"] = str(request.base_url) + '/' + str(new_bag.key.id) # <----change when deployed
        return res, 201

    # View all bags with pagination
    elif request.method == 'GET':
        jot = False
        if 'Authorization' in request.headers:
            jot = True
            # VERIFY JWT FIRST-----------------------------------------401
            payload = verify_jwt(request)
        cursor = request.args.get('cursor', default = None, type = str)
        query = client.query(kind=constants.bags)
        if jot == False:
            query.add_filter('private', "=", False)
        else:
            # filter query to bags by owner = sub's datastore id
            findUser = client.query(kind=constants.users)
            users = list(findUser.fetch())
            for member in users:
                if member['auth_id'] == payload['sub']:
                    u = member.key.id
            query.add_filter('owner', '=', str(u))
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
            # create object array for items each bag is carrying
            item_list = []
            if e["items"]:
                for i in e["items"]:
                    temp = {"id": i, "self": str(request.url_root) + 'items/' + str(i)}
                    item_list.append(temp)
                e["items"] = item_list
        # build res object
        res = {"count": len(list(query.fetch()))}
        res["bags"] = cur_results
        if next_url:
            res["next"] = next_url
        
        return res

    else:
        res = {"Error":  "Illegal request on root /bags"}

        return res, 405

# View or delete a bag by ID
@bp.route('/<id>', methods=['GET','PUT', 'PATCH', 'DELETE'])
def bags_get_delete(id):
    # VERIFY JWT FIRST-----------------------------------------401
    payload = verify_jwt(request)
    bag_key = client.key(constants.bags, int(id))
    bag = client.get(key=bag_key)
    if not bag:
        res = {"Error": "The specified bag does not exist"}
        return res, 404
    if not bag['owner']:
        res = {"Error": "only bags registered to users can be requested individually"}
        return res, 403
# check if bag belongs to another user------------------------- 403
    query = client.query(kind=constants.users)
    users = list(query.fetch())
    for member in users:
        if member['auth_id'] == payload['sub']:
            if not member['bags'] or bag.key.id not in member['bags']:
                res = {"Error":  "The bag belongs to another user" }
                return res, 403
    if request.method == 'GET':
        # check if accepted request is json
        if 'application/json' not in request.headers.get('Accept') and \
        request.headers.get('Accept') != "*/*":
            res = {"Error":  "Requested a MIME type unsupported by endpoint"}
            return res, 406  

        bag["id"] = bag.key.id
        item_list = []
        if bag["items"]:
            for i in bag["items"]:
                temp = {"id": i, "self": str(request.url_root) + 'items/' + str(i)}
                item_list.append(temp)
            bag["items"] = item_list
        bag["self"] = str(request.base_url) # <----change when deployed
        return jsonify(bag)

    elif request.method == 'DELETE': 
        # remove bag from user's list
        user_key = client.key(constants.users, int(bag['owner']))
        user = client.get(key=user_key)
        user['bags'].remove(bag.key.id)
        if len(user['bags']) == 0:
            user['bags'] = None      
        client.put(user)
        client.delete(bag_key)
        # remove the bag from items that have bag_id as a carrier
        query = client.query(kind=constants.items)
        results = list(query.fetch())
        for e in results:
            if e["carrier"] and e["carrier"]["id"] == bag.key.id:
                e.update({"carrier": None})
                client.put(e)

        return ('',204)

    elif request.method == 'PUT' or request.method == 'PATCH':
        #convert json to a dictionary
        content = request.get_json()
        if "model" in content:
            bag.update({"model": content["model"]})
        if "brand" in content:
            bag.update({"brand": content["brand"]})
        if "private" in content:
            bag.update({"private": content["private"]})
        
        client.put(bag)

        return ('',204)
        
    else:
        res = {"Error":  "Illegal request on root /bags"}

        return res, 405

"""

LOGISTICS -- LOGISTICS -- LOGISTICS -- LOGISTICS -- LOGISTICS -- LOGISTICS

"""
# add or remove an item from a bag
@bp.route('/<item_id>/<bag_id>', methods=['PUT','DELETE'])
def add_delete_item(item_id,bag_id):
    # VERIFY JWT FIRST---------------------------------------401
    payload = verify_jwt(request)
    # grab the bag object
    bag_key = client.key(constants.bags, int(bag_id))
    bag = client.get(key=bag_key)
    # grab the item object
    item_key = client.key(constants.items, int(item_id))
    item = client.get(key=item_key)
    # check if bag or item exists
    if not bag or not item:
        res = {"Error": "The specified bag and/or item does not exist"}
        return res, 404
    if not bag['owner']:
        res = {"Error": "can only put items in bags with owners"}
        return res, 403
# check if bag belongs to another user------------------------- 403
    query = client.query(kind=constants.users)
    users = list(query.fetch())
    for member in users:
        if member['auth_id'] == payload['sub']:
            if not member['bags'] or bag.key.id not in member['bags']:
                res = {"Error":  "bag owner must match owner credentials" }
                return res, 403

    if request.method == 'PUT':
        # check if item already assigned to the bag
        if bag["items"]:
            if item.key.id in bag["items"]:
                res = {"Error": "The item already assigned to this bag"}
                return res, 403
        # check if item is already in another bag
        elif item["carrier"] and item["carrier"]["id"] != bag.key.id:
            res = {"Error": "The item is still inside another bag"}
            return res, 403

        # else update item and bag
        item.update({"carrier": {"id": bag.key.id, "brand": bag["brand"]}})
        client.put(item)
        if not bag["items"]:
            bag.update({"items": [item.key.id]})
        else: 
            # make copy of items list, insert and replace
            temp = bag["items"].copy()
            temp.append(item.key.id)
            bag.update({"items": temp})   
        client.put(bag)
        return ('', 204)

    if request.method == 'DELETE':
        if bag and item:
            if not bag["items"] or item.key.id not in bag["items"]:
                res = {"Error": "No bag with this bag_id carries a item with this item_id"}
                return res, 403
            # remove item id from bag and carrier from item
            else:
                bag["items"].remove(item.key.id)
                # if removing the item causes attribute to be empty, change value [] to None
                if not bag["items"]:
                    bag.update({"items": None})
                client.put(bag)
                item.update({"carrier": None})
                client.put(item)
                return ('', 204)
    
    else:
        res = {"Error":  "Illegal request on root /bags"}
        return res, 405


# Register a bag to a user
@bp.route('/<bag_id>/users/<user_id>', methods=['PUT'])
def reg_bag(bag_id, user_id):
    # VERIFY JWT FIRST---------------------------------------401
    payload = verify_jwt(request)
    # grab the bag object
    bag_key = client.key(constants.bags, int(bag_id))
    bag = client.get(key=bag_key)
    # grab the user object w datastore user_id
    user_key = client.key(constants.users, int(user_id))
    user = client.get(key=user_key)
    if not bag or not user:
        res = {"Error":  "The specified bag or user does not exist"}
        return res, 404
    if user['auth_id'] != payload['sub']:
        res = {"Error":  "user token and ID don’t match"}
        return res, 403
    # ignore owner alert if same owner is re-reg their bag on accident  
    if bag['owner'] and bag['owner'] != str(user_id):
        res = {"Error":  "The bag belongs to another user"}
        return res, 403

    if request.method == 'PUT':
    #convert json to a dictionary
        content = request.get_json()
        if not user["bags"]:
            user['bags'] = []
        user['bags'].append(bag.key.id)
        client.put(user)
    # update privacy settings on bag
        if 'private' in content:
            bag.update({"private": content['private'], "owner": user_id})
        client.put(bag)
        return ('', 204)

    else: 
        res = {"Error":  "Illegal request on root /bags"}
        return res, 405


