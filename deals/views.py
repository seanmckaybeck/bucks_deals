import flask
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import HTTPException

from .mailgun import mailgun_notify
from . import db, admin
from .forms import ItemForm, PercentForm
from .models import UnapprovedItem, Item, Spot


deals_blueprint = flask.Blueprint('deals', __name__)
from . import errors
ITEM_DB = db.Base("items")
SPOT_DB = db.Base("spot")
UNAPPROVED_DB = db.Base("unapproved")


@deals_blueprint.route('/')
def index(page=1):
    select = PercentForm()
    sp = next(SPOT_DB.fetch())
    it = next(ITEM_DB.fetch())
    spots = list(Spot(**s) for s in sp)
    items = list(Item(**i) for i in it)
    return flask.render_template('index.html', items=items, spots=spots, select=select)


@deals_blueprint.route('/about')
def about():
    return flask.render_template('about.html')


@deals_blueprint.route('/contact')
def contact():
    return flask.render_template('contact.html')


@deals_blueprint.route('/item/<item_id>', methods=['GET', 'POST'])
def item(item_id):
    i = ITEM_DB.get(item_id)
    if i is None:
        flask.abort(404)
    i = Item(**i)
    spot = Spot(**next(SPOT_DB.fetch(query={"name": i.metal}))[0])
    if flask.request.method == 'POST':
        if i.reported:
            flask.flash('This item has already been reported', 'warning')
        else:
            mailgun_params = {
                              'api_key': flask.current_app.config['MAILGUN_API_KEY'],
                              'domain': flask.current_app.config['MAILGUN_DOMAIN'],
                              'subject': 'Item reported',
                              'to': flask.current_app.config['MAILGUN_ADMIN'],
                              'from': flask.current_app.config['MAILGUN_FROM'],
                              'text': 'A user has reported item {}'.format(item_id)
                             }
            mailgun_notify(**mailgun_params)
            i.reported = True
            ITEM_DB.put(i.dict())
            flask.flash("Thanks for the report! We'll look into it.", 'success')
    return flask.render_template('item.html', item=i, spot=spot)


@deals_blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ItemForm()
    if form.validate_on_submit():
        u = next(UNAPPROVED_DB.fetch({"ebay_id": form.item.data}))  # list of 1 or 0
        i = next(ITEM_DB.fetch({"ebay_id": form.item.data}))
        if not u and not i:
            UNAPPROVED_DB.put({"ebay_id": form.item.data})
            flask.flash('Item submitted for approval. Thank you.', 'success')
            mailgun_params = {
                              'api_key': flask.current_app.config['MAILGUN_API_KEY'],
                              'domain': flask.current_app.config['MAILGUN_DOMAIN'],
                              'subject': 'Item submitted',
                              'to': flask.current_app.config['MAILGUN_ADMIN'],
                              'from': flask.current_app.config['MAILGUN_FROM'],
                              'text': f'A user has submitted an item: http://ebay.com/itm/{form.item.data}'
                             }
            mailgun_notify(**mailgun_params)
            return flask.redirect(flask.url_for('deals.index'))
        else:
            flask.flash('That item has already been submitted.', 'warning')
    return flask.render_template('submit.html', form=form)


class HiddenView(ModelView):
    def is_accessible(self):
        auth = flask.request.authorization or flask.request.environ.get('REMOTE_USER')
        if not auth or (auth.username, auth.password) != flask.current_app.config['ADMIN_CREDS']:
            raise HTTPException('', flask.Response('Please log in', 401, {'WWW-Authenticate': 'Basic realm="Login required"'}))
        return True


class ItemView(HiddenView):
    form_excluded_columns = ('picture',)


# TODO: implement custom ModelView for Deta
# https://flask-admin.readthedocs.io/en/latest/adding_a_new_model_backend/#adding-model-backend
# admin.add_view(HiddenView(UnapprovedItem, db.session))
# admin.add_view(ItemView(Item, db.session))
# admin.add_view(HiddenView(Spot, db.session))
