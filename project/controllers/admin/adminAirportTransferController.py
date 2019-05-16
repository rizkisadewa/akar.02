# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField
from functools import wraps

#import from Model
from project.models.adminTripModel import adminTripModel

# an object from Admin Models
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

# Choose the Country
@app.route('/admin/airport-transfer-setting')
@is_logged_in
def airportTransferChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminAirportTransferSelectCountry.html', country_data=country_data)
