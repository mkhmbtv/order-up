from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from ..forms import TableAssignementForm
from ..models import MenuItem, MenuItemType, db, Employee, Order, Table

bp = Blueprint('orders', __name__, url_prefix='')


@bp.route('/')
@login_required
def index():
    assign_form = TableAssignementForm()
    open_tables, servers = open_tables_and_servers()
    assign_form.tables.choices = [(t.id, f"Table {t.number}") for t in open_tables]
    assign_form.servers.choices = [(s.id, s.name) for s in servers]

    orders = Order.query \
        .filter(Order.employee_id == current_user.id) \
        .filter(Order.finished is False) \
        .all()

    menu_items = MenuItem.query.join(MenuItemType) \
                         .order_by(MenuItemType.name, MenuItem.name) \
                         .all()

    return render_template('orders.html',
                           assign_form=assign_form,
                           orders=orders,
                           menu_items=menu_items)


@bp.route('/tables/assign', methods=['POST'])
def assign_table():
    table_id = request.form.get('tables')
    employee_id = request.form.get('servers')
    order = Order(table_id=table_id, employee_id=employee_id, finished=False)
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('.index'))


def open_tables_and_servers():
    tables = Table.query.order_by(Table.number).all()
    open_orders = Order.query.filter(Order.finished is False)
    busy_tables_ids = [order.table_id for order in open_orders]
    open_tables = [table for table in tables if table.id not in busy_tables_ids]
    servers = Employee.query.all()
    return open_tables, servers
