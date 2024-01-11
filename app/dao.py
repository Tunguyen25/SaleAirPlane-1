from app.models import User, Ticket, flightScheduling, Airport, Flight, Passenger
from app import app, db
import hashlib
import cloudinary.uploader
from sqlalchemy import or_, func
from sqlalchemy.orm import aliased


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


def add_passenger_info(name, phone, citizenId):
    p = Passenger(name=name, phone=phone, citizenId=citizenId)
    db.session.add(p)
    db.session.commit()


def get_airport():
    return Airport.query.all()


def get_flightScheduling(airportfrom,airportto):
    departure_airport_alias= aliased(Airport)
    arrival_airport_alias = aliased(Airport)

    flightSchedules = (flightScheduling.query.join(departure_airport_alias, flightScheduling.airportFrom_id == departure_airport_alias.id) \
        .join(arrival_airport_alias, flightScheduling.airportTo_id == arrival_airport_alias.id).filter(departure_airport_alias.name == airportfrom) or
                       (arrival_airport_alias.name == airportto))


    # for item in flightSchedules:
    #     if item is None:
    #         print("Found None object:", item)
    #
    #     return item

    return flightSchedules.all()


def count_flight():
    return db.session.query(Flight.id, Flight.flight,
                            func.count(flightScheduling.id)).join(flightScheduling,
                                                                  flightScheduling.flight_id == Flight.id,
                                                                  isouter=True).group_by(Flight.id).all()


def count_revenue():
    revenue = db.session.query(Flight.id, Flight.flight, func.sum(Ticket.price * Flight.numFlighted)).join(Flight,
                                                                                                           Ticket.id == Flight.id)

    return revenue.group_by(Flight.id).all()


if __name__ == '__main__':
    with app.app_context():
        print(get_flightScheduling(airportfrom='TP.Hồ Chí Minh', airportto='Cà Mau'))
