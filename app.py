import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        user = json.loads(request.date)
        new_user_obj = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user_obj)
        db.session.commit()
        db.session.close()
        return "Пользователь создан в базе данных", 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Не найдено"
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()

        return f"Объект с id {user_id} успешно изменен", 200
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()

        return f"Объект с id {user_id} успешно удален", 200


@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        res = []
        for order in Order.query.all():
            res.append(order.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        try:
            order = json.loads(request.date)
            month_start, day_start, year_start = [int(_) for _ in order['start_date'].split("/")]
            month_end, day_end, year_end = order['end_date'].split("/")
            new_order_obj = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=year_start, month=month_start, day=day_start),
                end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict())


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        res = []
        for offer in Offer.query.all():
            res.append(offer.to_dict())
        return jsonify(res)
    if request.method == 'POST':
        offer = json.loads(request.date)
        new_offer_obj = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано в базе данных", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено"
        else:
            return jsonify(offer.to_dict())


if __name__ == '__main__':
    app.run()
