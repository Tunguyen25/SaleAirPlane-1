import math

from flask import render_template, request, redirect, session, jsonify
import dao
import utils
from app import app, login, db
from app.models import flightScheduling, Ticket
from flask_login import login_user, logout_user, login_required


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)

    return render_template('login.html')


@app.route('/admin/login', methods=['post'])
def process_admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password, avatar=request.files.get('avatar'))
            except Exception as ex:
                print(str(ex))
                err_msg = 'Vui lòng nhập đầy đủ thông tin!'
            else:
                return redirect('/login.html')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('/register.html', err_msg=err_msg)


@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/login")


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/ticket')
def ticket():
    data = flightScheduling.query
    print(data)
    departure = request.args.get('departure')
    arrival = request.args.get('arrival')

    flightSchedules = dao.get_flightScheduling(airportfrom=departure, airportto=arrival)

    return render_template('ticket.html', flightSchedules=flightSchedules, data=data)


@app.route('/detail_passenger')
def cart():
    return render_template('detail_passenger.html')


@app.route('/detail_passenger', methods=['get', 'post'])
def pay_user():
    err_msg = None

    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        citizenId = request.form.get('citizenId')
        try:
            dao.add_passenger_info(name=request.form.get('name'),
                                   phone=request.form.get('phone'), citizenId=request.form.get('citizenId'))
        except Exception as ex:
            print(str(ex))
            err_msg = 'Vui lòng nhập đầy đủ thông tin!'
        else:
            return redirect('/pay_ticket.html')

    return render_template('/detail_passenger.html', err_msg=err_msg)


@app.route('/pay_ticket')
def pay_ticket():
    data = flightScheduling.query.all()

    # name = request.args.get('name')
    # phone = request.args.get('phone')
    # citizenId = request.args.get('citizenId')
    return render_template('pay_ticket.html', data=data)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
