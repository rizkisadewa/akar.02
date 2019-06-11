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
    service_id = StringField()

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

# Airport Transfer Setting
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
        service_id = form.service_id.data
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
        airport_transfer_data=airport_transfer_data,
        trip_data=trip_data,
        service_data=service_data
    )

# Airport Transfer Update Data
@app.route('/admin/aiport-transfer/<string:country>/<string:destination>/<string:trip_id>/edit/<string:airport_transfer_id>', methods=['GET','POST'])
@is_logged_in
def airportTransferDataUpdate(country, destination, trip_id, airport_transfer_id):

    # Fetch One Airport Transfer
    airport_transfer_data = adminAirportTransferModel.airportTransferDataFetchOne(airport_transfer_id)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Service Data
    service_data = adminServiceModel.serviceDataFetchOne(trip_id)

    # fit the Airport Transfer Form Class
    form = AddAirportTransferData(request.form)

    # Populate Airport Transfer form fields
    form.airport_transfer_title.data = airport_transfer_data['airport_transfer_title']
    form.inclusions.data = airport_transfer_data['inclusions']
    form.pickup_point.data = airport_transfer_data['pickup_point']
    form.drop_off_point.data = airport_transfer_data['drop_off_point']
    form.duration.data = airport_transfer_data['duration']
    form.airport_transfer_description.data = airport_transfer_data['airport_transfer_description']

    # Update Airport Transfer Data
    if request.method == 'POST' and form.validate():

        # Asign the variable value from request form value
        airport_transfer_title = request.form['airport_transfer_title']
        inclusions = request.form['inclusions']
        pickup_point = request.form['pickup_point']
        drop_off_point = request.form['drop_off_point']
        duration = request.form['duration']
        airport_transfer_description = request.form['airport_transfer_description']
        service_id = request.form['service_id']

        # Execute the query
        adminAirportTransferModel.updateAirportTransferData(airport_transfer_title, inclusions, pickup_point, drop_off_point, duration, airport_transfer_description, service_id, airport_transfer_id)

        # Send the notification to the dashboard
        flash('Airport Transfer has been updated', 'success')

        return redirect(url_for('airportTransferDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminAirportTransferEdit.html',
        form=form,
        destination=destination,
        airport_transfer_data=airport_transfer_data,
        country=country,
        trip_data=trip_data,
        service_data=service_data
    )

# Airport Transfer Delete Data
@app.route('/admin/aiport-transfer/<string:country>/<string:destination>/<string:trip_id>/delete/<string:airport_transfer_id>', methods=['GET','POST'])
@is_logged_in
def deleteAirportTransfer(country, destination, trip_id, airport_transfer_id):

    # Execute the query of delte from the model
    adminAirportTransferModel.deleteAirportTransfer(airport_transfer_id)

    # Send the notification to the Dashboard
    flash('Airport Transfer has been deleted', 'danger')

    # Return to the Airport Transfer Center page
    return redirect(url_for('airportTransferDataCenter', country=country, destination=destination, trip_id=trip_id))
