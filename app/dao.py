from app.models import User, Ticket, flightScheduling, Airport
from app import app, db
import hashlib
import cloudinary.uploader
from sqlalchemy import or_, func


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


def load_flightSchedules(kw=None):
    flightSchedules = flightScheduling.query

    if kw:
        # tickets = flightSchedules.filter(flightScheduling.arrival_airport.has(kw))
        flightSchedules = flightSchedules.join(flightScheduling.arrival_airport).filter(Airport.name.contains(kw))

    return flightSchedules.all()


if __name__ == '__main__':
    with app.app_context():
        print(load_flightSchedules(kw="Hà Nội"))
