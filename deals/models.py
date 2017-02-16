from . import db


class UnapprovedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ebay_id = db.Column(db.Integer, unique=True)

    def __init__(self, ebay_id):
        self.ebay_id = ebay_id

    def __repr__(self):
        return 'UnapprovedItem(%d)' % self.ebay_id


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ebay_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    weight = db.Column(db.Float)
    metal = db.Column(db.String)
    picture_url = db.Column(db.String)
    reported = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)
    quantity = db.Column(db.Integer, default=0)
    seller = db.Column(db.String)

    def to_json(self):
        j = {
             'ebay_id': self.ebay_id,
             'name': self.name,
             'price': self.price,
             'weight': self.weight,
             'metal': self.metal,
             'picture_url': self.picture_url,
             'reported': self.reported,
             'available': self.available,
             'quantity': self.quantity,
             'seller': self.seller
            }
        return j

    def __repr__(self):
        return 'Item(%d, %s, %f, %f, %s, ...)' % (self.ebay_id, self.name, self.price, self.weight, self.metal)


class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    value = db.Column(db.Float)

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return 'Spot(%s, %f)' % (self.name, self.value)

