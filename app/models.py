import enum, datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean, CHAR
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from app import db,app
from datetime import datetime
from werkzeug.routing import Rule





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
    ticket = relationship('Ticket', back_populates='user')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    def __str__(self):
        return self.name


class Passenger(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(CHAR(100), nullable=False)
    citizenId = Column(CHAR(50), nullable=False)
    ticket = relationship('Ticket', back_populates='passenger')

    def __str__(self):
        return self.name


class Flight(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight = Column(String(100), nullable=False, unique=False)
    revenue = Column(Integer, nullable=False)
    numFlighted = Column(Integer, nullable=False)
    tickets_id = relationship('Ticket', back_populates='flight', foreign_keys='Ticket.flight_id')
    flight_scheduling = relationship('flightScheduling', backref='flight')

    def __str__(self):
        return f"Flight(id={self.id}, flight={self.flight}, revenue={self.revenue})"


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


class Rules(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    minimumtime = Column(DateTime, default=datetime.now(), nullable=False)
    totallyairpotsub = Column(Integer, nullable=False)
    timestop = Column(DateTime, default=datetime.now(), nullable=False)
    tickets = relationship('Ticket', back_populates='rule')
    flight_scheduling = relationship('flightScheduling', back_populates='rule')

    def __str__(self):
        return f"Rules(id={self.id}, minimumtime={self.minimumtime}, totallyairpotsub={self.totallyairpotsub}, timestop={self.timestop})"


class Ticket(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    rankTicket = Column(String(50), nullable=False, unique=True)
    price = Column(Float, default=0)
    flight_id = Column(Integer, ForeignKey(Flight.id), nullable=False)
    flight = relationship('Flight', back_populates='tickets_id')
    flight_scheduling = relationship('flightScheduling', back_populates='ticket')
    passenger_id = Column(Integer, ForeignKey(Passenger.id))
    passenger = relationship('Passenger', back_populates='ticket')
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='ticket')
    rule_id = Column(Integer, ForeignKey(Rules.id), nullable=False)
    rule = relationship('Rules', back_populates='tickets')
    status = Column(Boolean, nullable=False)
    # setTime = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f"Ticket(id={self.id}, flight_id={self.flight_id}, rule_id={self.rule_id})"


class Staff(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(CHAR(100), nullable=False)
    gioitinh = Column(String(50), unique=False)
    flight_scheduling = relationship('flightScheduling', back_populates='staff')
    employee_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.EMPlOYEE)

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
    rule_id = Column(Integer, ForeignKey(Rules.id))
    rule = relationship('Rules', back_populates='flight_scheduling')
    staff_id = Column(Integer, ForeignKey(Staff.id))
    staff = relationship('Staff', back_populates='flight_scheduling')

    def __str__(self):
        return f"flightScheduling(id={self.id}, flight_id={self.flight_id}, rule_id={self.rule_id})"


if __name__ == '__main__':
    from app import app

    with app.app_context():
        # db.create_all()

        # import hashlib
        #
        # u = User(name='Van A', username='Van A',
        #          password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.USER)
        #
        # u1 = User(name='Van B', username='Van B',
        #          password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.USER)
        #
        # u2 = User(name='Van C', username='Van C',
        #          password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.USER)
        #
        # a = User(name='Admin', username='admin',
        #          password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.ADMIN)
        #
        # e = User(name='NV1', username='NV1',
        #          password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.EMPlOYEE)
        #
        # db.session.add_all([u,u1,u2,a,e])
        # db.session.commit()

        f = Flight(id='1', flight='Air Asia', revenue='200000000', numFlighted='3')
        f1 = Flight(id='2', flight='AirLines', revenue='500000000 ', numFlighted='5')
        f2 = Flight(id='3', flight='DragonAir', revenue='40000000 ', numFlighted='2')
        db.session.add_all([f, f1, f2])
        db.session.commit()

        p = Passenger(id='1', name='Van A', phone='093333311', citizenId='079231313')
        p1 = Passenger(id='2', name='Van B', phone='093233333', citizenId='07823133333')
        p2 = Passenger(id='3', name='Van C', phone='0935453333', citizenId='078243433333')
        db.session.add_all([p, p1,p2])
        db.session.commit()

        r = Rules(id='1', minimumtime=None, totallyairpotsub='3', timestop=None)
        r1 = Rules(id='2', minimumtime=None, totallyairpotsub='2', timestop=None)
        r2 = Rules(id='3', minimumtime=None, totallyairpotsub='1', timestop=None)
        db.session.add_all([r, r1, r2])
        db.session.commit()

        t1 = Ticket(id='2', rankTicket='Hạng 2', price='2000000', flight_id='2', passenger_id='1', user_id='1',
                    rule_id='1', status=True)
        t = Ticket(id='1', rankTicket='Hạng 1', price='2500000', flight_id='1', passenger_id='2', user_id='2',
                   rule_id='2',status=False)
        t2 = Ticket(id='3', rankTicket='Hạng 3', price='5500000', flight_id='3', passenger_id='3', user_id='3',
                    rule_id='3',status=True)
        db.session.add_all([t, t1, t2])
        db.session.commit()

        a = Airport(id='1',name='TP.Hồ Chí Minh')
        a1 = Airport(id='2', name='Hà Nội')
        a2 = Airport(id='3' ,name='Đà Nẵng')
        a3 = Airport(id='4' ,name='Hải Phòng')
        a4 = Airport(id='5' ,name='Cà Mau')
        db.session.add_all([a, a1, a2, a3,a4])
        db.session.commit()

        s = AirportSup(id='1',name='Quy Nhơn',timeRelax='30', note='Bay đã', airport_id='1')
        s1 = AirportSup(id='2',name='Nha Trang', timeRelax='20', note='Bay xa', airport_id='2')
        s2 = AirportSup(id='3',name='ĐắK LắK', timeRelax='30', note='Bay đi luôn', airport_id='3')
        db.session.add_all([s, s1, s2])
        db.session.commit()

        f = flightScheduling(flight_id='1', airportFrom_id='1', airportTo_id='2', airportSup_id='1',
                             dateTime='2024-9-10', flightTime='1 tiếng', numSeat1='5A', numSeat2='9B', ticket_id='1')
        f1 = flightScheduling(flight_id='2', airportFrom_id='4', airportTo_id='3', airportSup_id='2',
                              dateTime='2023-10-11', flightTime='2 tiếng', numSeat1='1A', numSeat2='8A', ticket_id='2')
        f2 = flightScheduling(flight_id='3', airportFrom_id='1', airportTo_id='5', airportSup_id='3',
                              dateTime='2024-1-10', flightTime='30 phút', numSeat1='2A', numSeat2='7A', ticket_id='3')
        f3 = flightScheduling(flight_id='1', airportFrom_id='4', airportTo_id='2', airportSup_id='3',
                              dateTime='2024-8-10', flightTime='3 tiếng', numSeat1='3A', numSeat2='6A', ticket_id='3')
        f4 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='3', airportSup_id='2',
                              dateTime='2024-9-20', flightTime='4 tiếng', numSeat1='4A', numSeat2='5A', ticket_id='2')
        f5 = flightScheduling(flight_id='3', airportFrom_id='4', airportTo_id='5', airportSup_id='1',
                              dateTime='2024-1-20', flightTime='2 tiếng', numSeat1='5A', numSeat2='4A', ticket_id='1')
        f6 = flightScheduling(flight_id='2', airportFrom_id='1', airportTo_id='2', airportSup_id='1',
                              dateTime='2024-5-13', flightTime='3 tiếng', numSeat1='6A', numSeat2='3A', ticket_id='1')
        f7 = flightScheduling(flight_id='3', airportFrom_id='4', airportTo_id='3', airportSup_id='3',
                              dateTime='2024-4-20', flightTime='5 tiếng', numSeat1='7A', numSeat2='2A', ticket_id='2')
        f8 = flightScheduling(flight_id='1', airportFrom_id='1', airportTo_id='5', airportSup_id='3',
                              dateTime='2024-6-10', flightTime='3 tiếng', numSeat1='8A', numSeat2='1A', ticket_id='3')
        f9 = flightScheduling(flight_id='2', airportFrom_id='4', airportTo_id='2', airportSup_id='2',
                              dateTime='2024-9-5', flightTime='4 tiếng', numSeat1='9A', numSeat2='5A', ticket_id='3')
        f10 = flightScheduling(flight_id='3', airportFrom_id='1', airportTo_id='3', airportSup_id='1',
                              dateTime='2024-8-5', flightTime='2 tiếng', numSeat1='10A', numSeat2='6A', ticket_id='2')
        f11 = flightScheduling(flight_id='1', airportFrom_id='4', airportTo_id='5', airportSup_id='2',
                              dateTime='2024-9-5', flightTime='4 tiếng', numSeat1='11A', numSeat2='7A', ticket_id='1')
        db.session.add_all([f, f1, f2, f3, f4, f5, f6, f7, f8, f9,f10,f11])
        db.session.commit()

        s = Staff(id='1', name='NV1', phone='09893819031', gioitinh='Nam', employee_role=UserRoleEnum.EMPlOYEE)
        db.session.add(s)
        db.session.commit()
