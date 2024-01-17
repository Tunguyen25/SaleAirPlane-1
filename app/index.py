import math

from flask import render_template, request, redirect, session, jsonify, flash
import dao
import utils
from app import app, login, db,generate_random_otp,client, verified_number, verify_sid
from app.models import flightScheduling, Ticket
from flask_login import login_user, logout_user, login_required
from datetime import datetime
from flask_mail import Mail
from twilio.rest import Client


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
                return redirect('/login')
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
    departure = request.args.get('departure')
    arrival = request.args.get('arrival')
    data = dao.get_flightScheduling(departure, arrival)

    return render_template('ticket.html', data=data)


@app.route('/detail_passenger')
def cart():
    return render_template('detail_passenger.html')


@app.route('/api/ticket', methods=['post'])
def add_to_ticket():
    data = request.json
    ticket = session.get('ticket')
    if ticket is None:
        ticket = {}
    id = str(data.get("id"))
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

        # ve chua co
    ticket[id] = {
            "id": id,
            # "name":data.get('name'),
            "departure":data.get('departure'),
            "arrival":data.get('arrival'),
            "price": data.get('price'),
            "booking_time": formatted_time
    }

    session['ticket'] = ticket

    return jsonify(dao.count_ticket(ticket))


@app.route('/api/ticket/<ticket_id>', methods=['delete'])
def delete_ticket(ticket_id):
    ticket = session.get('ticket')
    if ticket and ticket_id in ticket:
        del ticket[ticket_id]

    session['ticket'] = ticket
    return jsonify(dao.count_ticket(ticket))


@app.route('/send_otp', methods=['POST'])
def send_otp():
    if request.method.__eq__('POST'):
        phone_number = request.form.get('phone')
        if phone_number:
            generated_otp = generate_random_otp()
            phone_number_ = '+84' + phone_number

            # Gửi tin nhắn SMS
            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=phone_number_, channel="sms")
            flash('Mã OTP đã được gửi đến số điện thoại của bạn.')

            # Lưu thông tin vào session
            session['phone_number'] = phone_number
            session['generated_otp'] = generated_otp

            return redirect('/detail_passenger')
        else:
            flash('Vui lòng nhập số điện thoại.')

    return render_template('detail_passenger.html')


@app.route('/detail_passenger', methods=['get', 'post'])
def pay_user():
    err_msg = None

    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        citizenId = request.form.get('citizenId')
        submitted_otp = request.form.get('otp')
        if not name or not phone or not citizenId or not submitted_otp:
            err_msg = 'Vui lòng nhập đầy đủ thông tin và mã OTP.'
        else:
            generated_otp = request.form.get('generated_otp')
            if submitted_otp == session.get('generated_otp'):
                try:
                    dao.add_passenger_info(name=request.form.get('name'),
                                           phone=request.form.get('phone'), citizenId=request.form.get('citizenId'))

                except Exception as ex:
                    print(str(ex))
                    err_msg = 'Vui lòng nhập đầy đủ thông tin!'
                else:
                    return redirect('/detail_passenger')
            else:
                err_msg = 'Mã OTP không đúng. Vui lòng thử lại.'

    return render_template('/detail_passenger.html', err_msg=err_msg)


@app.context_processor
def common_responses():
    return {
        'tickets': dao.get_ticket(),
        'ticket_stats': dao.count_ticket(session.get('ticket'))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
