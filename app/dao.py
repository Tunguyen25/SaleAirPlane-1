from flask import session

from app.models import User, Ticket, flightScheduling, Airport, Flight, Passenger
from app import app, db
import hashlib
import cloudinary.uploader
from sqlalchemy import or_, func
from sqlalchemy.orm import aliased
from flask import request, flash
from flask_mail import Message
import secrets
import pyotp


def get_user_by_id(id):
    return User.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username, password=password)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


def add_ticket_info(id,price, flight, passenger, status):
    t = Ticket(id=id,price=price,flight=flight,passenger=passenger,status=status)
    db.session.add(t)
    db.session.commit()


def add_passenger_info(name, phone, citizenId):
    p = Passenger(name=name, phone=phone, citizenId=citizenId)
    db.session.add(p)
    db.session.commit()


# def save_user_after_otp_verification(name, phone, citizenId,email):
#     # Kiểm tra và xác thực mã OTP
#     submitted_otp = request.form.get('otp')  # Thay thế bằng cách lấy dữ liệu từ form
#     if verify_otp(submitted_otp, email):
#         # Nếu mã OTP đúng, thực hiện lưu vào database
#         p = Passenger(name=name, phone=phone, citizenId=citizenId)
#
#         db.session.add(p)
#         db.session.commit()
#     else:
#         # Xử lý khi mã OTP không đúng
#         flash('Mã OTP không đúng. Vui lòng thử lại.')


def get_airport():
    return Airport.query.all()


def get_ticket():
    return Ticket.query.all()


def get_flightSchedules():
    return flightScheduling.query.all()


def get_flightScheduling(departure, arrival):
    departure_airport_alias= aliased(Airport)
    arrival_airport_alias = aliased(Airport)
    a = flightScheduling.query
    if  departure and arrival:
        a = a.join(departure_airport_alias, flightScheduling.airportFrom_id == departure_airport_alias.id) \
            .join(arrival_airport_alias, flightScheduling.airportTo_id == arrival_airport_alias.id).filter(departure_airport_alias.name == departure, arrival_airport_alias.name == arrival)

    return  a.all()



def count_flight():
    return db.session.query(Flight.id, Flight.flight,
                            func.count(flightScheduling.id)).join(flightScheduling,
                                                                  flightScheduling.flight_id == Flight.id,
                                                                  isouter=True).group_by(Flight.id).all()

#
# def count_revenue():
#     revenue = db.session.query(Flight.id, Flight.flight, func.sum(Ticket.price * Flight.numFlighted)).join(Flight,
#                                                                                                            Ticket.id == Flight.id)
#
#     return revenue.group_by(Flight.id).all()

def stats_flight(month):
    result = (
        db.session.query(
            Flight.flight,
            func.sum(Flight.numFlighted * Ticket.price).label('total_revenue'),
            func.count(flightScheduling.id).label('total_flights')#Đếm số lượt bay.
    # Tính tổng doanh thu.
        )
        .join(flightScheduling, Flight.id == flightScheduling.flight_id)
        .join(Ticket, Flight.id == Ticket.flight_id)
        .filter(
            func.extract('month', flightScheduling.dateTime) == month, #Trích xuất tháng từ
        )
        .group_by(Flight.id)
        .all()
    )

    # result = (
    #     db.session.query(
    #         Flight.flight,
    #         func.sum(flightScheduling.numSeat1 + flightScheduling.numSeat2).label('total_flights'),
    #         func.sum(flightScheduling.numSeat1 + flightScheduling.numSeat2 * Ticket.price).label('total_revenue')
    #     )
    #     .join(flightScheduling, Flight.id == flightScheduling.flight_id)
    #     .join(Ticket, Flight.id == Ticket.flight_id)
    #     .filter(
    #         func.extract('month', flightScheduling.dateTime) == month
    #     )
    #     .group_by(Flight.id)
    #     .all()
    # )

    # In kết quả
    # for flight, total_revenue, total_flights in result:
    #     print(
    #         f"Flight: {flight}, Total Revenue: {total_revenue}, Total Flights: {total_flights}"
    #     )
    return result


def sum_revenue(month):
    tong = 0
    for i in stats_flight(month):
        tong += i.total_revenue
    return  tong


def count_ticket(ticket):
    total_price = 0
    if ticket:
        for c in ticket.values():
            total_price += c["price"]
    return {"total_price":total_price}



if __name__ == '__main__':
    with app.app_context():
        count_ticket(ticket='')
