import enum, datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, CHAR
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPlOYEE = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(100), default=None)

    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight = Column(String(100), nullable=False, unique=False)
    revenue = Column(Integer, nullable=False)
    numFlighted = Column(Integer, nullable=False)
    tickets = relationship('Ticket', back_populates='flight', foreign_keys='Ticket.flight_id')
    flight_scheduling = relationship('flightScheduling', backref='flight')

    def __str__(self):
        return self.name


class Airport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    airportSup = relationship('AirportSup', back_populates='airports')
    departure_schedules = relationship('flightScheduling', back_populates='departure_airport',
                                       foreign_keys='flightScheduling.airportFrom_id')
    arrival_schedules = relationship('flightScheduling', back_populates='arrival_airport',
                                     foreign_keys='flightScheduling.airportTo_id')

    def __str__(self):
        return self.name


class AirportSup(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    timeRelax = Column(Integer, nullable=True)
    note = Column(CHAR(100))
    airport_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airports = relationship('Airport', back_populates='airportSup')
    flight_schedules = relationship('flightScheduling', back_populates='airportSup')

    def __str__(self):
        return self.name


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    rankTicket = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    flight = relationship('Flight', back_populates='tickets')
    passenger = relationship('Passenger', back_populates='ticket')
    flight_scheduling = relationship('flightScheduling', back_populates='ticket')

    def __str__(self):
        return self.name


class flightScheduling(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    airportFrom_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airportTo_id = Column(Integer, ForeignKey(Airport.id), nullable=False)
    airportSup_id = Column(Integer, ForeignKey(AirportSup.id), nullable=True)
    dateTime = Column(DateTime, default=datetime.now())
    flightTime = Column(String(50), nullable=False, unique=False)
    numSeat1 = Column(String(10), nullable=False, unique=False)
    numSeat2 = Column(String(10), nullable=False, unique=False)
    activate = Column(Boolean, default=True)
    departure_airport = relationship('Airport', back_populates='departure_schedules', foreign_keys=[airportFrom_id])
    arrival_airport = relationship('Airport', back_populates='arrival_schedules', foreign_keys=[airportTo_id])
    airportSup = relationship('AirportSup', back_populates='flight_schedules')
    ticket_id = Column(Integer, ForeignKey(Ticket.id))
    ticket = relationship('Ticket', back_populates='flight_scheduling')

    def __str__(self):
        return self.name


class Passenger(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(CHAR(100), nullable=False)
    citizenId = Column(CHAR(50), nullable=False)
    ticket_id = Column(Integer, ForeignKey(Ticket.id), nullable=False)
    ticket = relationship('Ticket', back_populates='passenger')

    def __str__(self):
        return self.name


class Staff(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(CHAR(100), nullable=False)
    gioitinh = Column(String(50), unique=False)

    employee_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.EMPlOYEE)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    from app import app

    with app.app_context():
        # db.create_all()

        import hashlib

        # u = User(name='Admin', username='admin',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        # u1 = User(name='Danh', username='danh',
        #           password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #           user_role=UserRoleEnum.ADMIN)

        # e = User(name='NV1', username='NV1',
        #           password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #           user_role=UserRoleEnum.EMPlOYEE)
        #
        # db.session.add(e)
        # db.session.commit()

        # db.session.add_all([u, u1])
        # db.session.commit()

        # f = Flight(id='1', flight='Air Asia', revenue='200000000', numFlighted='3')
        # f1 = Flight(id='2', flight='AirLines', revenue='500000000 ', numFlighted='5')
        # f2 = Flight(id='3', flight='DragonAir', revenue='40000000 ', numFlighted='2')
        # db.session.add_all([f, f1, f2])
        # db.session.commit()
        #
        # t1 = Ticket(id='2', rankTicket='Hạng 2', price='2000000', flight_id='2')
        # t = Ticket(id='1', rankTicket='Hạng 1', price='2500000', flight_id='1')
        # t2 = Ticket(id='3', rankTicket='Hạng 3', price='5500000', flight_id='3')
        # db.session.add_all([t, t1, t2])
        # db.session.commit()
        #
        # a = Airport(id='1',name='TP.Hồ Chí Minh')
        # a1 = Airport(id='2', name='Hà Nội')
        # a2 = Airport(id='3' ,name='Đà Nẵng')
        # db.session.add_all([a, a1, a2])
        # db.session.commit()
        #
        # s = AirportSup(id='1',name='Quy Nhơn',timeRelax='30', note='Bay đã', airport_id='1')
        # s1 = AirportSup(id='2',name='Nha Trang', timeRelax='20', note='Bay xa', airport_id='2')
        # s2 = AirportSup(id='3',name='ĐắK LắK', timeRelax='30', note='Bay đi luôn', airport_id='3')
        # db.session.add_all([s, s1, s2])
        # db.session.commit()
        #
        # f = flightScheduling(flight_id='1', airportFrom_id='1', airportTo_id='2', airportSup_id='1',
        #                      dateTime='2023-11-12', flightTime='1 tiếng', numSeat1='5A', numSeat2='9B', ticket_id='1')
        # f1 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='2', airportSup_id='2',
        #                       dateTime='2023-10-4', flightTime='2 tiếng', numSeat1='1A', numSeat2='8A', ticket_id='2')
        # f2 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='2', airportSup_id='3',
        #                       dateTime='2023-10-4', flightTime='30 phút', numSeat1='2A', numSeat2='7A', ticket_id='3')
        # f3 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='3', airportSup_id='3',
        #                       dateTime='2023-10-4', flightTime='3 tiếng', numSeat1='3A', numSeat2='6A', ticket_id='3')
        # f4 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='3', airportSup_id='2',
        #                       dateTime='2023-10-4', flightTime='4 tiếng', numSeat1='4A', numSeat2='5A', ticket_id='2')
        # f5 = flightScheduling(flight_id='2', airportFrom_id='2', airportTo_id='3', airportSup_id='1',
        #                       dateTime='2023-10-4', flightTime='2 tiếng', numSeat1='5A', numSeat2='4A', ticket_id='1')
        # f6 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='2', airportSup_id='1',
        #                       dateTime='2023-10-4', flightTime='3 tiếng', numSeat1='6A', numSeat2='3A', ticket_id='1')
        # f7 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='3', airportSup_id='3',
        #                       dateTime='2023-10-4', flightTime='5 tiếng', numSeat1='7A', numSeat2='2A', ticket_id='2')
        # f8 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='2', airportSup_id='3',
        #                       dateTime='2023-10-4', flightTime='3 tiếng', numSeat1='8A', numSeat2='1A', ticket_id='3')
        # f9 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='3', airportSup_id='2',
        #                       dateTime='2023-10-4', flightTime='4 tiếng', numSeat1='9A', numSeat2='5A', ticket_id='3')
        # db.session.add_all([f, f1, f2, f3,f4,f5,f6,f7,f8,f9])
        # db.session.commit()
        #
        # p = Passenger(id='1', name='Van A', phone='093333311', citizenId='079231313', ticket_id='1')
        # p1 = Passenger(id='2', name='Van B', phone='093233333', citizenId='07823133333', ticket_id='2')
        # db.session.add_all([p, p1])
        # db.session.commit()

        s = Staff(id='1', name='NV1', phone='09893819031',gioitinh='Nam', employee_role=UserRoleEnum.EMPlOYEE)
        s1 = Staff(id='2', name='NV2', phone='90183901033',gioitinh='Nữ',employee_role=UserRoleEnum.EMPlOYEE)
        db.session.add_all([s, s1])
        db.session.commit()
