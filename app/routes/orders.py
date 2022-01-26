from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..forms import MenuItemAssignementForm, TableAssignementForm
from ..models import (
    db, Employee, MenuItem, MenuItemType, Order, OrderDetail, Table
)

bp = Blueprint('orders', __name__, url_prefix='')


@bp.route('/')
@login_required
def index():
    form = TableAssignementForm()
    open_tables, servers = open_tables_and_servers()
    form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    form.servers.choices = [(s.id, s.name) for s in servers]

    orders = Order.query \
        .filter(Order.employee_id == current_user.id) \
        .filter(Order.finished == False)

    menu_items = MenuItem.query.join(MenuItemType) \
                         .order_by(MenuItemType.name, MenuItem.name) \
                         .options(db.joinedload(MenuItem.type))

    foods_by_type = {}
    for menu_item in menu_items:
        if menu_item.type.name not in foods_by_type:
            foods_by_type[menu_item.type.name] = []
        foods_by_type[menu_item.type.name].append(menu_item)

    return render_template('orders.html',
                           form=form,
                           orders=orders,
                           foods_by_type=foods_by_type)


@bp.route('/orders/<int:id>/items', methods=['POST'])
def add_to_order(id):
    form = MenuItemAssignementForm()
    form.menu_item_ids.choices = [(i.id, '') for i in MenuItem.query.all()]
    if form.validate_on_submit():
        order = Order.query.get(id)
        for menu_item_id in form.menu_item_ids.data:
            db.session.add(OrderDetail(order=order, menu_item_id=menu_item_id))
        db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/orders/assign', methods=['POST'])
def assign_table():
    form = TableAssignementForm()
    open_tables, servers = open_tables_and_servers()
    form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    form.servers.choices = [(s.id, s.name) for s in servers]

    if form.validate_on_submit():
        table_id = request.form.get('tables')
        employee_id = request.form.get('servers')
        order = Order(table_id=table_id, employee_id=employee_id, finished=False)
        db.session.add(order)
        db.session.commit()
    return redirect(url_for('.index'))


@bp.route('/orders/<int:id>/close', methods=['POST'])
def close_table(id):
    order = Order.query.get(id)
    order.finished = True
    db.session.commit()
    return redirect(url_for('.index'))


def open_tables_and_servers():
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished == False)
    busy_tables_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_tables_ids]
    servers = Employee.query.all()
    return open_tables, servers
