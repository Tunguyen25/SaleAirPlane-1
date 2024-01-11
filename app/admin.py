from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, dao, db
from flask_login import logout_user, current_user
from app.models import Ticket, Passenger, Flight, flightScheduling, Airport, AirportSup, UserRoleEnum, Rules
from flask import redirect


class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_flight())


admin = Admin(app=app, name='Quản trị viên', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedStaff(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.EMPlOYEE


class MyTicketView(AuthenticatedAdmin):
    column_list = ['id', 'rankTicket', 'price', 'flight_id', 'flight.flight', 'passenger']


class MyPassengerView(AuthenticatedAdmin):
    column_list = ['name', 'phone', 'citizenId', 'ticket.id']


class MyFlightView(AuthenticatedAdmin):
    column_list = ['flight', 'revenue', 'numFlighted']


class MyFlightSchedulingView(AuthenticatedAdmin):
    column_list = ['flight_id', 'airportFrom_id', 'airportTo_id', 'airportSup_id', 'dateTime',
                   'flightTime', 'numSeat1', 'numSeat2', 'departure_airport', 'arrival_airport', 'airportSup.name',
                   'ticket.price']
    can_export = True
    column_searchable_list = ['numSeat1', 'numSeat2', 'ticket.price']
    column_filters = ['ticket.price']
    column_editable_list = ['departure_airport', 'arrival_airport']
    details_modal = True
    edit_modal = True


class MyAirportView(AuthenticatedAdmin):
    column_list = ['name']


class MyAirportSupView(AuthenticatedAdmin):
    column_list = ['timeRelax', 'note', 'airport_id', 'airports']


class MyStaffView(AuthenticatedStaff):
    column_list = ['flight_id', 'airportFrom_id', 'airportTo_id', 'airportSup_id', 'dateTime',
                   'flightTime', 'numSeat1', 'numSeat2', 'departure_airport', 'arrival_airport', 'airportSup.name',
                   'ticket.price']


class MyStaffTicketView(AuthenticatedStaff):
    column_list = ['rankTicket', 'price', 'flight_id', 'flight', 'flight_scheduling', 'passenger_id', 'passenger',
                   'user_id', 'user', 'rule_id', 'rule']


class MyRulesView(AuthenticatedAdmin):
    column_list = ['minimumtime', 'totallyairpotsub', 'timestop']
    column_editable_list = ['minimumtime', 'totallyairpotsub', 'timestop']
    details_modal = True
    edit_modal = True


class StatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyRulesView(Rules, db.session))
admin.add_view(MyAirportView(Airport, db.session))
admin.add_view(MyAirportSupView(AirportSup, db.session))
admin.add_view(MyPassengerView(Passenger, db.session))

# Nhân Viên
admin.add_view(MyStaffView(flightScheduling, db.session))
admin.add_view(MyStaffTicketView(Ticket, db.session))


admin.add_view(StatsView(name='Thông kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
