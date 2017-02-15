from collections import defaultdict
import json
import os

from ebaysdk.shopping import Connection
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import requests

from deals import create_app, db
from deals.models import Item, Spot, UnapprovedItem


path = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(path, 'config.py')
app = create_app(config)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create():
    """Create an empty database"""
    db.create_all()


@manager.command
def destroy():
    """Destroy the existing database"""
    db.drop_all()


@manager.command
def add(ebay_id, name, price, weight, metal):
    """Add a new item to the database"""
    ebay_id = int(ebay_id)
    price = float(price)
    weight = float(weight)
    item = Item.query.filter_by(ebay_id=ebay_id).first()
    if item is None:
        item = Item(ebay_id, name, price, weight, metal)
        db.session.add(item)
        db.session.commit()


@manager.command
def delete(ebay_id):
    """Delete the specified item"""
    ebay_id = int(ebay_id)
    item = Item.query.filter_by(ebay_id=ebay_id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()


@manager.command
def spot(name, value):
    """Add a new spot type to the database"""
    spot = Spot.query.filter_by(name=name).first()
    if spot is None:
        spot = Spot(name, value)
    else:
        spot.value = value
    db.session.add(spot)
    db.session.commit()


@manager.command
def update_spot():
    """Update the values of all existing spots"""
    spots = Spot.query.all()
    r = requests.get('http://spot.seanmckaybeck.com/api/all')
    r.raise_for_status()
    for metal in spots:
        spot = Spot.query.filter_by(name=metal.name).first()
        spot.value = r.json()[metal.name]
        db.session.add(spot)
        db.session.commit()


@manager.command
def update_items():
    """Update the prices, quantities, and availability of all items in the database"""
    items = Item.query.all()
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    for item in items:
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id), 'IncludeSelector': 'Details'})
        except:
            print('call failed for {}'.format(item.ebay_id))
            continue
        item.price = float(r.dict()['Item']['ConvertedCurrentPrice']['value'])
        quantity = int(r.dict()['Item']['Quantity']) - int(r.dict()['Item']['QuantitySold'])
        item.quantity = quantity
        item.available = True if quantity > 0 else False
        db.session.add(item)
    db.session.commit()


@manager.command
def pictures():
    """Set the picture_url for all items in the database"""
    items = Item.query.all()
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    for item in items:
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id), 'IncludeSelector': 'Details'})
        except:
            print('call failed for {}'.format(item.ebay_id))
            continue
        item.picture_url = r.dict()['Item']['PictureURL'][0]
        db.session.add(item)
    db.session.commit()


@manager.command
def picture(ebay_id):
    """Set the picture_url for the specified item"""
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    item = Item.query.filter_by(ebay_id=ebay_id).first()
    if item:
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id), 'IncludeSelector': 'Details'})
        except:
            print('call failed for {}'.format(item.ebay_id))
            return
        item.picture_url = r.dict()['Item']['PictureURL'][0]
        db.session.add(item)
        db.session.commit()
    else:
        print('No item with that ID')


@manager.command
def exportdb():
    """Export the database to a JSON file called data.json"""
    items = Item.query.all()
    spots = Spot.query.all()
    uns = UnapprovedItem.query.all()
    data = defaultdict(list)
    for item in items:
        i = {}
        i['name'] = item.name
        i['ebay_id'] = item.ebay_id
        i['price'] = item.price
        i['weight'] = item.weight
        i['metal'] = item.metal
        i['reported'] = item.reported
        i['picture_url'] = item.picture_url
        i['available'] = item.available
        i['quantity'] = item.quantity
        data['items'].append(i)
    for spot in spots:
        s = {}
        s['name'] = spot.name
        s['value'] = spot.value
        data['spots'].append(s)
    for un in uns:
        u = {}
        u['ebay_id'] = un.ebay_id
        data['unapproved'].append(u)
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))


@manager.command
def importdb():
    """Import a database from a JSON file called data.json"""
    with open('data.json') as f:
        data = json.load(f)
    for item in data['items']:
        i = Item(item['ebay_id'], item['name'], item['price'],
                 item['weight'], item['metal'], item['reported'],
                 item['available'], item['picture_url'], item['quantity'])
        db.session.add(i)
    for spot in data['spots']:
        s = Spot(spot['name'], spot['value'])
        db.session.add(s)
    for unapproved in data['unapproved']:
        u = UnapprovedItem(unapproved['ebay_id'])
        db.session.add(u)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

