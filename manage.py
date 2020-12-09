from collections import defaultdict
import json
import os

from ebaysdk.shopping import Connection
from flask_script import Manager
import requests

from deals import create_app, db
from deals.models import Item, Spot, UnapprovedItem


path = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(path, 'config.py')
app = create_app(config)
manager = Manager(app)
ITEM_DB = db.Base("items")
SPOT_DB = db.Base("spot")
UNAPPROVED_DB = db.Base("unapproved")


@manager.command
def add(ebay_id, name, price, weight, metal):
    """Add a new item to the database"""
    ebay_id = int(ebay_id)
    price = float(price)
    weight = float(weight)
    item = next(ITEM_DB.fetch(query={"ebay_id": ebay_id}))
    if not item:
        item = Item(**{'ebay_id': ebay_id, 'name': name,
                       'price': price, 'weight': weight, 'metal': metal})  # verifies all good
        ITEM_DB.put(item.dict())


@manager.command
def delete(ebay_id):
    """Delete the specified item"""
    ebay_id = int(ebay_id)
    item = next(ITEM_DB.fetch(query={"ebay_id": ebay_id}))
    if item:
        ITEM_DB.delete(item[0]['key'])


@manager.command
def spot(name, value):
    """Add a new spot type to the database"""
    spot = next(SPOT_DB.fetch(query={"name": name}))
    if not spot:
        spot = Spot(name=name, value=value)
        SPOT_DB.put(**spot.dict())
    else:
        spot[0]['value'] = value
        SPOT_DB.put(spot[0])


@manager.command
def update_spot():
    """Update the values of all existing spots"""
    spots = next(SPOT_DB.fetch())
    r = requests.get('http://spot.seanmckaybeck.com/api/all')  # TODO: this doesnt exist
    r.raise_for_status()
    for metal in spots:
        spot = Spot(**metal)
        spot.value = r.json()[spot.name]
        SPOT_DB.put(spot.dict())


@manager.command
def update_items():
    """Update the prices, quantities, and availability of all items in the database"""
    items = list(ITEM_DB.fetch())
    items = [Item(**i) for i in items[0]]
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    for item in items:
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id), 'IncludeSelector': 'Details'})
        except:
            print('call failed for {}'.format(item.ebay_id))
            continue
        d = r.dict()
        if d['Item']['ListingStatus'] == 'Completed':
            ITEM_DB.delete(item.key)
        else:
            item.price = float(d['Item']['ConvertedCurrentPrice']['value'])
            quantity = int(d['Item']['Quantity']) - int(r.dict()['Item']['QuantitySold'])
            item.quantity = quantity
            item.available = True if quantity > 0 else False
            item.picture_url = d['Item']['PictureURL'][0]
            item.seller = d['Item']['Seller']['UserID']
            ITEM_DB.put(item.dict())


@manager.command
def update_item(ebay_id):
    """Update the info for the specified item"""
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    item = next(ITEM_DB.fetch(query={"ebay_id": ebay_id}))
    if item:
        item = Item(**item[0])
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id), 'IncludeSelector': 'Details'})
        except:
            print('call failed for {}'.format(item.ebay_id))
            return
        item.price = float(r.dict()['Item']['ConvertedCurrentPrice']['value'])
        quantity = int(r.dict()['Item']['Quantity']) - int(r.dict()['Item']['QuantitySold'])
        item.quantity = quantity
        item.available = True if quantity > 0 else False
        item.picture_url = r.dict()['Item']['PictureURL'][0]
        item.seller = r.dict()['Item']['Seller']['UserID']
        ITEM_DB.put(item.dict())
    else:
        print('No item with that ID')


# @manager.command
# def exportdb():
#     """Export the database to a JSON file called data.json"""
#     items = Item.query.all()
#     spots = Spot.query.all()
#     uns = UnapprovedItem.query.all()
#     data = defaultdict(list)
#     for item in items:
#         data['items'].append(item.to_json())
#     for spot in spots:
#         s = {}
#         s['name'] = spot.name
#         s['value'] = spot.value
#         data['spots'].append(s)
#     for un in uns:
#         u = {}
#         u['ebay_id'] = un.ebay_id
#         data['unapproved'].append(u)
#     with open('data.json', 'w') as f:
#         f.write(json.dumps(data))


# @manager.command
# def importdb():
#     """Import a database from a JSON file called data.json"""
#     with open('data.json') as f:
#         data = json.load(f)
#     for item in data['items']:
#         i = Item(**item)
#         db.session.add(i)
#     for spot in data['spots']:
#         s = Spot(spot['name'], spot['value'])
#         db.session.add(s)
#     for unapproved in data['unapproved']:
#         u = UnapprovedItem(unapproved['ebay_id'])
#         db.session.add(u)
#     db.session.commit()


if __name__ == '__main__':
    manager.run()
