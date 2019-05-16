# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField, IntegerField
from functools import wraps

#import from Model
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel
from project.models.adminAirportTransferModel import adminAirportTransferModel

# an object from Admin Models
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()
adminAirportTransferModel = adminAirportTransferModel()

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

# Add Airport Transfer Data Form Class
class AddAirportTransferData(Form):
    airport_transfer_title = StringField(u'Airport Transfer Title')
    airport_transfer_description = TextAreaField(u'Airport Transfer Description')
    inclusions = StringField(u'Airport Transfer Inclusions')
    duration = IntegerField(u'Duration in Minutes')
    pickup_point = StringField("Pickup Point")
    drop_off_point = StringField("Drop Off Point")

# Choose the Country
@app.route('/admin/airport-transfer-setting')
@is_logged_in
def airportTransferChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminAirportTransferSelectCountry.html', country_data=country_data)

# Choose the Destination
@app.route('/admin/airport-transfer-setting/<string:country>')
@is_logged_in
def airportTransferChooseDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminTripModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminTripModel.destinationFetchOne(country)

    return render_template(
        'admin/adminAirportTransferSelectDestination.html',
        destination_data=destination_data,
        country_data_fetch_one=country_data_fetch_one)

# Airport Transfer Excursions Setting
@app.route('/admin/airport-transfer-setting/<string:country>/<string:destination>/<string:trip_id>', methods=['GET','POST'])
@is_logged_in
def airportTransferDataCenter(country, destination, trip_id):

    # Fitting the class
    form = AddAirportTransferData(request.form)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Service Data
    service_data = adminServiceModel.serviceDataFetchOne(trip_id)

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Fetch Airport Transfer Data
    airport_transfer_data = adminAirportTransferModel.airportTransferFetchData(trip_id)

    # Add the Data
    if request.method == 'POST' and form.validate():
        service_id = service_data['service_id']
        admin_id = admin_data['admin_id']
        airport_transfer_title = form.airport_transfer_title.data
        inclusions = form.inclusions.data
        pickup_point = form.pickup_point.data
        drop_off_point = form.drop_off_point.data
        duration = form.duration.data
        airport_transfer_description = form.airport_transfer_description.data

        # Execute Query
        adminAirportTransferModel.addAirportTransferData(service_id, admin_id, airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description)

        # Send the Notification
        flash('Airport Transfer Added', 'success')

        return redirect(url_for('airportTransferDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminAirportTransferDataCenter.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        form=form,
        airport_transfer_data=airport_transfer_data
    )
