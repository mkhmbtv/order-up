from dotenv import load_dotenv
from random import randint
load_dotenv()

from app import app, db
from app.models import (
    Employee,
    Menu, MenuItem,
    MenuItemType,
    Order, OrderDetail,
    Table
)


with app.app_context():
    db.drop_all()
    db.create_all()

    employee = Employee(
        name='Margot',
        employee_number=1234,
        password='password'
    )

    beverages = MenuItemType(name="Beverages")
    entrees = MenuItemType(name="Entrees")
    sides = MenuItemType(name="Sides")

    dinner = Menu(name="Dinner")

    fries = MenuItem(name="French fries", price=3.50, type=sides, menu=dinner)
    drp = MenuItem(name="Dr. Pepper", price=1.0, type=beverages, menu=dinner)
    jambalaya = MenuItem(name="Jambalaya", price=21.98, type=entrees, menu=dinner)

    for i in range(1, 11):
        db.session.add(Table(number=i, capacity=randint(2, 8)))

    table = Table(number=11, capacity=4)
    order = Order(employee=employee, table=table, finished=False)
    order_detail = OrderDetail(order=order, menu_item=fries)

    db.session.add(dinner)
    db.session.add(employee)
    db.session.add(order)
    db.session.commit()
