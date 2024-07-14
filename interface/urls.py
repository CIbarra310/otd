from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('production_admin', views.production_admin, name="production_admin"),
    path('user_admin', views.user_admin, name="user_admin"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('driver_roster', views.driver_roster, name="driver_roster"),
    path('add_driver', views.add_driver, name="add_driver"),
    path('activate_driver/<int:driver_id>/', views.activate_driver, name='activate_driver'),
    path('deactivate_driver/<int:driver_id>/', views.deactivate_driver, name='deactivate_driver'),
    path('driver/<int:driver_id>/', views.view_driver, name='view_driver'),
    path('driver_rundown', views.driver_rundown, name='driver_rundown'),
    path('new_run', views.new_run, name="new_run"),
    path('run_history', views.run_history, name="run_history"),
    path('run_queue', views.run_queue, name="run_queue"),
    path('run/<int:run_request_id>/', views.view_run, name='view_run'),
    path('complete_run/<int:run_request_id>/', views.complete_run, name="complete_run"),
    path('cancel_run/<int:run_request_id>/', views.cancel_run, name="cancel_run"),
    path('radios', views.radios, name="radios"),
    path('radio_scan', views.radio_scan, name="radio_scan"),
    path('change_production', views.change_production, name="change_production"),
]