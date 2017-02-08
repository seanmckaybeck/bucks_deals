from flask import abort
from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from .mailgun import mailgun_notify

from . import db, admin
from .forms import ItemForm, PercentForm
from .models import UnapprovedItem, Item, Spot


deals_blueprint = Blueprint('deals', __name__)
from . import errors


@deals_blueprint.route('/')
@deals_blueprint.route('/<int:page>')
def index(page=1):
    select = PercentForm()
    spots = Spot.query.all()
    items = Item.query.order_by(Item.metal.desc()).paginate(page, current_app.config['PAGINATION'], True)
    return render_template('index.html', items_pagination=items, spots=spots, select=select)


@deals_blueprint.route('/about')
def about():
    return render_template('about.html')


@deals_blueprint.route('/contact')
def contact():
    return render_template('contact.html')


@deals_blueprint.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    i = Item.query.get(item_id)
    if i is None:
        abort(404)
    spot = Spot.query.filter_by(name=i.metal).first()
    if request.method == 'POST':
        if i.reported:
            flash('This item has already been reported', 'warning')
        else:
            mailgun_params = {
                              'api_key': current_app.config['MAILGUN_API_KEY'],
                              'domain': current_app.config['MAILGUN_DOMAIN'],
                              'subject': 'Item reported',
                              'to': current_app.config['MAILGUN_ADMIN'],
                              'from': current_app.config['MAILGUN_FROM'],
                              'text': 'A user has reported item {}'.format(item_id)
                             }
            mailgun_notify(**mailgun_params)
            i.reported = True
            db.session.add(i)
            db.session.commit()
            flash('Thanks for the report! We\'ll look into it', 'success')
    return render_template('item.html', item=i, spot=spot)


@deals_blueprint.route('/submit', methods=['GET', 'POST'])
def submit():
    form = ItemForm()
    if form.validate_on_submit():
        u = UnapprovedItem.query.filter_by(ebay_id=form.item.data).first()
        if not u:
            u = UnapprovedItem(form.item.data)
            db.session.add(u)
            db.session.commit()
            # maybe add sending an email to admin here
            flash('Item submitted for approval. Thank you.', 'success')
            return redirect(url_for('deals.index'))
        else:
            flash('That item has already been submitted.', 'warning')
    return render_template('submit.html', form=form)


admin.add_view(ModelView(UnapprovedItem, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(ModelView(Spot, db.session))

