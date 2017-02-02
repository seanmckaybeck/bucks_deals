from flask import abort
from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from . import db
from .forms import ItemForm
from .models import UnapprovedItem, Item


deals_blueprint = Blueprint('deals', __name__)
from . import errors


@deals_blueprint.route('/')
@deals_blueprint.route('/<int:page>')
def index(page=1):
    items = Item.query.order_by(Item.metal.desc()).paginate(page, current_app.config['PAGINATION'], True)
    return render_template('index.html', items_pagination=items)


@deals_blueprint.route('/about')
def about():
    return render_template('about.html')


@deals_blueprint.route('/contact')
def contact():
    return render_template('contact.html')


@deals_blueprint.route('/items/')
@deals_blueprint.route('/items/<int:page>')
def items(page=1):
    items = Item.query.paginate(page, current_app.config['PAGINATION'], True).items
    return render_template('items.html', items=items)


@deals_blueprint.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item(item_id):
    i = Item.query.get(item_id)
    if i is None:
        abort(404)
    if request.method == 'POST':
        if i.reported:
            flash('This item has already been reported', 'warning')
        else:
            # TODO send report email
            i.reported = True
            db.session.add(i)
            db.session.commit()
            flash('Thanks for the report! We\'ll look into it', 'success')
    return render_template('item.html', item=i)


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

