# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

# import from Model
from project.models.adminServiceModel import adminServiceModel
from project.models.adminTripModel import adminTripModel

# an object from Mode
adminServiceModel = adminServiceModel()
adminTripModel = adminTripModel()

# Check if logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login', 'danger')
            return redirect(url_for('adminLogin'))
    return wrap

# Admin Service Setting Choose Service
@app.route('/admin/service-setting/<string:country>/<string:destination>/<string:trip_id>')
@is_logged_in
def serviceSettingChooseService(country, destination, trip_id):

    # Fetch The Data
    service_data = adminServiceModel.serviceFetchData(trip_id)
    trip_data = adminTripModel.tripFetchData()

    return render_template(
        'admin/adminServiceSettingChooseService.html',
        service_data=service_data,
        country=country,
        destination=destination,
        trip_id=trip_id,
        trip_data=trip_data)

# Admin Service 
