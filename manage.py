import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

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


if __name__ == '__main__':
    manager.run()

