from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('production_admin', views.production_admin, name="production_admin"),
    path('add_production/', views.add_production, name='add_production'),
    
    path('location/<int:location_id>/', views.view_location, name='view_location'),
    path('location_admin', views.location_admin, name="location_admin"),
    path('add_location', views.add_location, name="add_location"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user_admin', views.user_admin, name="user_admin"),

    path('daily_rundown/', views.daily_rundown, name='daily_rundown'),
    path('add_driver_to_rundown/', views.add_driver_to_rundown, name='add_driver_to_rundown'),
    path('remove_driver_from_rundown/', views.remove_driver_from_rundown, name='remove_driver_from_rundown'),
    path('save_rundown/', views.save_rundown, name='save_rundown'),
    path('copy_rundown/', views.copy_rundown, name='copy_rundown'),
    path('search_active_drivers/', views.search_active_drivers, name='search_active_drivers'),
    path('api/driver_info/<int:driver_id>/', views.driver_info, name='driver_info'),

    path('add_driver', views.add_driver, name="add_driver"),
    path('driver_roster', views.driver_roster, name="driver_roster"),
    path('activate_driver/<int:driver_id>/', views.activate_driver, name='activate_driver'),
    path('deactivate_driver/<int:driver_id>/', views.deactivate_driver, name='deactivate_driver'),
    path('driver/<int:driver_id>/', views.view_driver, name='view_driver'),
    path('driver_rundown', views.driver_rundown, name='driver_rundown'),
    path('driver_times', views.driver_times, name="driver_times"),
    path('driver_times_view/', views.driver_times_view, name='driver_times_view'),
    path('driver_times_confirmation/', views.driver_times_confirmation, name='driver_times_confirmation'),
    path('driver_times_submit/', views.driver_times_submit, name='driver_times_submit'),
     path('driver-times-success/', views.driver_times_success, name='driver_times_success'),

    path('equipment_admin', views.equipment_admin, name="equipment_admin"),
    path('add_equipment', views.add_equipment, name="add_equipment"),
    path('equipment_list', views.equipment_list, name="equipment_list"),
    path('add_picture_cars', views.add_picture_cars, name="add_picture_cars"),  # New URL for adding picture cars

    path('new_run', views.new_run, name="new_run"),
    path('run_history', views.run_history, name="run_history"),
    path('run_queue', views.run_queue, name="run_queue"),
    path('acknowledge_run/<int:run_id>/', views.acknowledge_run, name='acknowledge_run'),
    path('run/<int:run_request_id>/', views.view_run, name='view_run'),
    path('run/<int:run_request_id>/', views.update_run, name='update_run'),
    path('complete_run/<int:run_request_id>/', views.complete_run, name="complete_run"),
    path('cancel_run/<int:run_request_id>/', views.cancel_run, name="cancel_run"),

    path('radios', views.radios, name="radios"),
    path('radio_scan', views.radio_scan, name="radio_scan"),
    path('change_production', views.change_production, name="change_production"),
    path('search_locations/', views.search_locations, name='search_locations'),
    path('search_user_by_email/', views.search_user_by_email, name='search_user_by_email'),
    path('get_user_details_by_email/', views.get_user_details_by_email, name='get_user_details_by_email'),
]