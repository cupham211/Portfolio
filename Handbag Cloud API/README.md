App URL: <https://final-phamchri.wl.r.appspot.com> Acct Creation URL: Same As Above 



Handbag API Spec

Cloud Application

Fall 2021

[Data Model](#_heading=h.30j0zll)

[Create a Bag](#_heading=h.tyjcwt)

[View a Bag](#_heading=h.z337ya) (protected)

[View all Bags](#_heading=h.1pxezwc) (protected)

[Update a Bag](#_heading=h.41mghml) (protected)

[Delete a Bag](#_heading=h.2lwamvv) /remove from a member (protected)

[Create an Item](#_heading=h.3cqmetx)

[View an Item](#_heading=h.3hv69ve)

[View all Items](#_heading=h.48pi1tg)

[Update an Item](#_heading=h.2fk6b3p)

[Delete an Item](#_heading=h.2koq656)

[Assign an Item to a Bag](#_heading=h.3bj1y38) (protected)

[Remove an Item from a Bag](#_heading=h.2hio093) (protected)

[View all items for a given Bag](#_heading=h.1nia2ey) (protected)

[View all Members](#_heading=h.2eclud0)



Assign a Bag to a Member (protected)


# Data Model
The app stores three kinds of entities in Datastore: Member, Bags, and Items.
## Members

|**Property**|**Data Type**|**Notes**|
| :- | :- | :- |
|id|Integer|The id of the bag. Datastore automatically generates it. |
|name|String|Name of the member.|
|age|Integer|The age of the member.|
|bags|Embedded array|Has id and link to owned bag for each element|
##
## Bags

|**Property**|**Data Type**|**Notes**|
| :- | :- | :- |
|id|Integer|The id of the bag. Datastore automatically generates it. |
|model|String|Name/Type of the bag.|
|brand|String|The name of the company that designed the bag.|
|private|Boolean|Indicates if the bag can be shown publicly|
|owner|Integer|Id of the member who owns this bag|
|items|Embedded array|Has id and link to item for each element|

## Items

|**Property**|**Data Type**|**Notes**|
| :- | :- | :- |
|id|Integer|The id of the item. Datastore automatically generates it. |
|name|String|The name of the item|
|carrier|Embedded entity|Contains id, brand, and link to the bag carrying the item|
|category|String|What kind of product is the item|
|create\_date|Date and Time|Date the item was created/modified|



# Create a Bag
Allows you to create a new bag.

|POST /bags|
| :- |
## Request
### Path Parameters
None
### Request Body
Required
### Request Body Format
JSON
### Request JSON Attributes

|**Name**|**Description**|**Required?**|
| :- | :- | :- |
|model|The name of the bag.|Yes|
|brand|The designer of the bag.|Yes|
||||
### Request Body Example

|<p>{</p><p>`    `"model": "Birkin",</p><p>`  `"brand": "Hermes"</p><p>}</p>|
| :- |
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|201 Created||
|Failure|400 Bad Request|If the request is missing any of the 2 required attributes, the bag must not be created, and 400 status code must be returned.|
### Response Examples
- Datastore will automatically generate an ID and store it with the entity being created. The app sends back this value in the response body as shown in the example.
- The items and owner attribute is initialized to null and does not need to be included in the body during creation of a bag. private is initialized to False as it's a new bag.
- The self attribute will contain the live link to the REST resource corresponding to this bag. In other words, this is the URL to get this newly created bag.  The self attribute is not stored in Datastore
#### *Success*

|<p></p><p>Status: 201 Created</p><p></p><p>{</p><p>`    `"model": "Birkin",</p><p>`    `"brand": "Hermes",</p><p>`  `"private": False,</p><p>`    `"owner": null,</p><p>`  `“items”: null,</p><p>`    `"self": "https://<your-app>/bags/123"</p><p>}</p>|
| :- |
#### *Failure*

|<p>Status: 400 Bad Request</p><p></p><p>{    </p><p>"Error":  "The request object is missing at least one of the required attributes"</p><p>}</p>|
| :- |

# View a Bag
Allows a member to GET an existing bag

|GET /bags/:bag\_id|
| :- |
## Request
## Path Parameters

|**Name**|**Description**|
| :- | :- |
|bag\_id|ID of the bag|
### Request Headers
Authorization token required
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK||
|Failure|404 Not Found|No bag with this bag\_id exists|
### Response Examples
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>"id": 123,</p><p>"model": "Birkin",</p><p>"brand": "Hermes",</p><p>"private": True,</p><p>"owner": 432590,</p><p>"items":[</p><p>{</p><p>"id": 5678,</p><p>"self":"https://appspot.com/items/5678"},</p><p>{</p><p>"id": 8765,</p><p>"self":"https://appspot.com/items/8765"}</p><p>],</p><p>"self": "https://<your-app>/bags/123"</p><p>}</p><p></p>|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "No bag with this bag\_id exists" </p><p>}</p>|
| :- |

# View all Bags
List all the bags.

|GET /bags|
| :- |
## Request
### Path Parameters
None
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK||
### Response Examples
- Viewing all bags implements pagination.
- 3 bags should be returned per page.
- There must be a ‘next’ link to get to the next page of results, except for the last page.
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>“bags”: [</p><p>{</p><p>"id": 123,</p><p>"name": "Sea Witch",</p><p>"type": "Catamaran",</p><p>"length": 28,</p><p>"items":[</p><p>{</p><p>"id": 5678,</p><p>"self":"https://appspot.com/items/5678"},</p><p>{</p><p>"id": 8765,</p><p>"self":"https://appspot.com/items/8765"}</p><p>],</p><p>"self": "https://<your-app>/bags/123"</p><p>},</p><p>{</p><p>"id": 456,</p><p>"name": "Adventure",</p><p>"type": "Sailbag",</p><p>"length": 50,</p><p>"items":[</p><p>{</p><p>`             `"id": 365,</p><p>"self":"https://appspot.com/items/365"},</p><p>{</p><p>"id": 4821,</p><p>"self":"https://appspot.com/items/4821"}</p><p>],</p><p>` `"self": "https://<your-app>/bags/456"</p><p>},</p><p>{</p><p>"id": 789,</p><p>"name": "Hocus Pocus",</p><p>"type": "Sailbag",</p><p>"length": 100,</p><p>"items":[</p><p>{</p><p>"id": 2624,</p><p>"self":"https://appspot.com/items/2624"},</p><p>{</p><p>"id": 9087,</p><p>"self":"https://appspot.com/items/9087"}</p><p>],</p><p>` `"self": "https://<your-app>/bags/789"</p><p>`                    	`},</p><p>` `],</p><p>“next”: “https://<your-app>/bags?cursor=path\_to\_next\_group”</p><p>}</p>|
| :- |

# Update a Bag
Edit information about a bag.

|PUT /bags/:bag\_id|
| :- |
|PATCH /bags/:bag\_id|
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|bag\_id|ID of the bag|
### Request Body
Required
### Request Body Format
JSON
### Request JSON Attributes

|**Name**|**Description**|**Required?**|
| :- | :- | :- |
|name|The name of the bag.|Yes|
|type|The type of the bag. E.g., Sailbag, Catamaran, etc.|Yes|
|length|Length of the bag in feet.|Yes|
### Request Body Example

|<p>{</p><p>`    `"name": "Sea Witch",</p><p>`  `"type": "Catamaran",</p><p>`    `"length": 28</p><p>}</p>|
| :- |
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content|Succeeds only if the bag\_id exists |
|Failure|404 Not Found|The specified bag does not exist|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
####
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "The specified bag does not exist" </p><p>}</p>|
| :- |
#

# Delete a Bag
Allows you to delete a bag. Note that deleting the bag dumps all items inside the bag.

|DELETE /bags/:bag\_id|
| :- |
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|bag\_id|ID of the bag|
### Request Body
None
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content||
|Failure|404 Not Found|No bag with this bag\_id exists|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "No bag with this bag\_id exists" </p><p>}</p>|
| :- |


# Create an Item
Allows you to create a new item.

|POST /items|
| :- |
## Request
### Path Parameters
None
### Request Body
Required
### Request Body Format
JSON
### Request JSON Attributes

|**Name**|**Description**|**Required?**|
| :- | :- | :- |
|volume|The size of the item|Yes|
|content|The type of items inside the item|Yes|
### Request Body Example

|<p>{</p><p>`    `"volume": 5,</p><p>`  `"content": "LEGO Blocks"</p><p>}</p>|
| :- |
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|201 Created||
|Failure|400 Bad Request|If the request is missing any required attribute, the item must not be created, and 400 status code must be returned.|
### Response Examples
- Datastore will automatically generate an ID and store it with the entity being created. This value needs to be sent in the response body as shown in the example.
- The value of the attribute carrier is the entity of the bag currently at this item. For a newly created bag the value of carrier should be null.
- The value of the attribute self is a live link to the REST resource corresponding to this item. In other words, this is the URL to get this newly created item. This attribute is not in Datastore.
#### *Success*

|<p>Status: 201 Created</p><p></p><p>{</p><p>`        	`"id": 123,</p><p>`        	 `"volume": 5,     </p><p>`        	`"carrier": null,</p><p>`        	`"content": "LEGO Blocks",</p><p>`        	`"creation\_date": "10/18/2020",</p><p>`         	`"self": "https://<your-app>/items/123"</p><p>}</p><p></p>|
| :- |
#### *Failure*

|<p>Status: 400 Bad Request</p><p></p><p>{    </p><p>"Error":  "The request object is missing at least one required attribute"</p><p>}</p>|
| :- |

# View an Item
Allows you to get an existing item.

|GET /items/:item\_id|
| :- |
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|item\_id|ID of the item|
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK||
|Failure|404 Not Found|No item with this item\_id exists|
### Response Examples
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>"id": 123,</p><p>volume": 5,     </p><p>"carrier": {</p><p>"id": 1234,</p><p>"name": "Sea Witch",</p><p>"self": "https://appspot.com/bags/1234"</p><p>},  </p><p>"content": "LEGO Blocks",</p><p>"creation\_date": "10/18/2020",</p><p>"self": "https://<your-app>/items/123"</p><p>}</p><p></p>|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "No item with this item\_id exists" </p><p>}</p>|
| :- |

# View all Items
List all the items.

|GET /items|
| :- |
## Request
### Path Parameters
None
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK||
### Response Examples
- Must be paginated with 3 per page and a ‘next’ link.
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>“items”: [</p><p>{</p><p>"id": 123,</p><p>"volume": 5,     </p><p>"carrier": {</p><p>"id": 1234,</p><p>"name": "Sea Witch",</p><p>"self": "https://appspot.com/bags/1234"</p><p>},  </p><p>"content": "LEGO Blocks",</p><p>"creation\_date": "10/18/2020"</p><p>"self": "https://<your-app>/items/123"</p><p>},</p><p>{</p><p>"id": 456,</p><p>"volume": 10,     </p><p>"carrier": {</p><p>"id": 789,</p><p>"name": "John Almos",</p><p>"self": "https://appspot.com/bags/789"</p><p>},  </p><p>"content": "Hammers",</p><p>"creation\_date": "10/19/2020"</p><p>"self": "https://<your-app>/items/456"</p><p>}</p><p>],</p><p>“next”: “https://<your-app>/items?cursor=path\_to\_next\_group”</p><p>}</p><p></p>|
| :- |
# Update an Item
Edit information about a bag.

|PUT /items/:item\_id|
| :- |
|PATCH /items/:item\_id|
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|item\_id|ID of the item|
### Request Body
Required
### Request Body Format
JSON
### Request JSON Attributes

|**Name**|**Description**|**Required?**|
| :- | :- | :- |
|name|The name of the bag.|Yes|
|type|The type of the bag. E.g., Sailbag, Catamaran, etc.|Yes|
|length|Length of the bag in feet.|Yes|
### Request Body Example

|<p>{</p><p>`    `"name": "Sea Witch",</p><p>`  `"type": "Catamaran",</p><p>`    `"length": 28</p><p>}</p>|
| :- |
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content|Succeeds only if the item\_id exists |
|Failure|404 Not Found|The specified item does not exist|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
####
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "The specified item does not exist" </p><p>}</p>|
| :- |
#
# Delete an Item
Allows you to delete an item. If the item being deleted was inside a bag, the bag must be updated.

|DELETE /items/:item\_id|
| :- |
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|item\_id|ID of the item|
### Request Body
None
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content||
|Failure|404 Not Found|No item with this item\_id exists|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "No item with this item\_id exists" </p><p>}</p>|
| :- |


# Assign an Item to a Bag
Place a item onto a bag.

|PUT /bags/:item\_id/:bag\_id|
| :- |
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|item\_id|ID of the item|
|bag\_id|ID of the bag|
### Request Body
None

Note: Set Content-Length to 0 in your request when calling out to this endpoint.
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content|Succeeds only if a bag exists with this bag\_id, a item exists with this item\_id, and the item isn’t already on a bag.|
|Failure|403 Forbidden|The item was already assigned to the bag.|
|Failure|403 Forbidden|There is already a bag with this item. |
|Failure|404 Not Found|The specified bag and/or item does not exist|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
####
#### *Failure*

|<p>Status: 403 Forbidden</p><p></p><p>{    </p><p>"Error":  "The item already assigned to this bag" </p><p>}</p>|
| :- |


|<p>Status: 403 Forbidden</p><p></p><p>{    </p><p>"Error":  "The item is still inside another bag" </p><p>}</p>|
| :- |


|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "The specified bag and/or item does not exist" </p><p>}</p>|
| :- |

## Comment
- A item cannot be assigned to multiple bags. However, bags can have multiple items.
# Remove an Item from a Bag
Removes a item from a bag without deleting that item.

|DELETE /bags/:item\_id/:bag\_id|
| :- |
## Request
### Path Parameters

|**Name**|**Description**|
| :- | :- |
|item\_id|ID of the item|
|bag\_id|ID of the bag|
### Request Body
None
## Response
No body
### Response Body Format
Success: No body 

Failure: JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|204 No Content|Succeeds only if a bag exists with this bag\_id, a item exists with this item\_id, and the bag carries that item.|
|Failure|403 Forbidden|bag\_id has no item with the item\_id|
|Failure|404 Not Found|The item and/or bag doesn’t exist|
### Response Examples
#### *Success*

|Status: 204 No Content|
| :- |
#### *Failure*

|<p>Status: 403 Not Found</p><p>{    </p><p>"Error":  "No bag with this bag\_id carries a item with this item\_id" </p><p>}</p>|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p>{    </p><p>"Error":  "The specified item and/or bag does not exist" </p><p>}</p>|
| :- |

# View all items for a given Bag
Shows all items on a bag with specific bag\_id

|GET /bags/:bag\_id/items|
| :- |
## Request
## Path Parameters

|**Name**|**Description**|
| :- | :- |
|bag\_id|ID of the bag|
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK|Succeeds if bag id exists|
|Failure|404 Not Found|No bag with this bag\_id exists|
### Response Examples
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>`    `"items":[</p><p>{</p><p>"id": 5678,</p><p>"self":https://appspot.com/items/5678</p><p>},</p><p>{</p><p>"id": 8765,</p><p>"self":https://appspot.com/items/8765</p><p>}</p><p>`    `]</p><p>}</p><p></p>|
| :- |
#### *Failure*

|<p>Status: 404 Not Found</p><p></p><p>{    </p><p>"Error":  "No bag with this bag\_id exists" </p><p>}</p>|
| :- |

# View all Members
List all the bags.

|GET /members|
| :- |
## Request
### Path Parameters
None
### Request Body
None
## Response
### Response Body Format
JSON
### Response Statuses

|**Outcome**|**Status Code**|**Notes**|
| :- | :- | :- |
|Success|200 OK||
### Response Examples
- Viewing all bags implements pagination.
- 3 bags should be returned per page.
- There must be a ‘next’ link to get to the next page of results, except for the last page.
#### *Success*

|<p>Status: 200 OK</p><p></p><p>{</p><p>“bags”: [</p><p>{</p><p>"id": 123,</p><p>"name": "Sea Witch",</p><p>"type": "Catamaran",</p><p>"length": 28,</p><p>"items":[</p><p>{</p><p>"id": 5678,</p><p>"self":"https://appspot.com/items/5678"},</p><p>{</p><p>"id": 8765,</p><p>"self":"https://appspot.com/items/8765"}</p><p>],</p><p>"self": "https://<your-app>/bags/123"</p><p>},</p><p>{</p><p>"id": 456,</p><p>"name": "Adventure",</p><p>"type": "Sailbag",</p><p>"length": 50,</p><p>"items":[</p><p>{</p><p>`             `"id": 365,</p><p>"self":"https://appspot.com/items/365"},</p><p>{</p><p>"id": 4821,</p><p>"self":"https://appspot.com/items/4821"}</p><p>],</p><p>` `"self": "https://<your-app>/bags/456"</p><p>},</p><p>{</p><p>"id": 789,</p><p>"name": "Hocus Pocus",</p><p>"type": "Sailbag",</p><p>"length": 100,</p><p>"items":[</p><p>{</p><p>"id": 2624,</p><p>"self":"https://appspot.com/items/2624"},</p><p>{</p><p>"id": 9087,</p><p>"self":"https://appspot.com/items/9087"}</p><p>],</p><p>` `"self": "https://<your-app>/bags/789"</p><p>`                    	`},</p><p>` `],</p><p>“next”: “https://<your-app>/bags?cursor=path\_to\_next\_group”</p><p>}</p>|
| :- |

Page 22** of 22**

