import os

from ebaysdk.shopping import Connection
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import requests

from deals import create_app, db
from deals.models import Item, Spot


path = os.path.abspath(os.path.dirname(__file__))
config = os.path.join(path, 'config.py')
app = create_app(config)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create():
    db.create_all()


@manager.command
def destroy():
    db.drop_all()


@manager.command
def add(ebay_id, name, price, weight, metal):
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
    ebay_id = int(ebay_id)
    item = Item.query.filter_by(ebay_id=ebay_id).first()
    if item is not None:
        db.session.delete(item)
        db.session.commit()


@manager.command
def spot(name, value):
    spot = Spot.query.filter_by(name=name).first()
    if spot is None:
        spot = Spot(name, value)
    else:
        spot.value = value
    db.session.add(spot)
    db.session.commit()


@manager.command
def update_spot():
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
    items = Item.query.all()
    api = Connection(appid=app.config['EBAY_APP_ID'], config_file=None)
    for item in items:
        try:
            r = api.execute('GetSingleItem', {'ItemID': str(item.ebay_id)})
        except:
            print('call failed for {}'.format(item.ebay_id))
        item.price = float(r.dict()['Item']['ConvertedCurrentPrice']['value'])
        db.session.add(item)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

