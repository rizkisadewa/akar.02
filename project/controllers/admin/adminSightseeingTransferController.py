# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField, IntegerField
from functools import wraps

#import from Model
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel
from project.models.adminSightseeingTransferModel import adminSightseeingTransferModel

# an object from Admin Models
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()
adminSightseeingTransferModel = adminSightseeingTransferModel()

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

# Add Sightseeing Transfer Data Form Class
class AddSightSeeingTransferData(Form):
    sightseeing_transfer_title = StringField(u'Sightseeing Transfer Title')
    sightseeing_transfer_description = TextAreaField(u'Sightseeing Transfer Description')
    inclusions = StringField(u'Sightseeing Transfer Inclusions')
    duration = IntegerField(u'Duration in Minutes')
    pickup_point = StringField("Pickup Point")
    drop_off_point = StringField("Drop Off Point")


# Choose the Country
@app.route('/admin/sightseeing-transfer-setting')
@is_logged_in
def sightseeingTransferChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminSightseeingTransferSelectCountry.html', country_data=country_data)

# Choose the Destination
@app.route('/admin/sightseeing-transfer-setting/<string:country>')
@is_logged_in
def sightseeingTransferChoooseDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminTripModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminTripModel.destinationFetchOne(country)

    return render_template(
        'admin/adminSightseeingTransferSelectDestination.html',
        destination_data=destination_data,
        country_data_fetch_one=country_data_fetch_one)

# Sightseeing Transfer Setting
@app.route('/admin/sightseeing-transfer-setting/<string:country>/<string:destination>/<string:trip_id>', methods=['GET','POST'])
@is_logged_in
def sightseeingTransferDataCenter(country, destination, trip_id):

    # Fiting the Form by the class
    form = AddSightSeeingTransferData(request.form)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Service Data
    service_data = adminServiceModel.serviceDataFetchOne(trip_id)

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Fetch Sightseeing Transfer
    sightseeing_transfer_data = adminSightseeingTransferModel.sightseeingTransferFetchData(trip_id)

    # Add the Data
    if request.method == 'POST' and form.validate():

        service_id = service_data['service_id']
        admin_id = admin_data['admin_id']
        sightseeing_transfer_title = form.sightseeing_transfer_title.data
        inclusions = form.inclusions.data
        pickup_point = form.pickup_point.data
        drop_off_point = form.drop_off_point.data
        duration = form.duration.data
        sightseeing_transfer_description = form.sightseeing_transfer_description.data

        # Execute Query
        adminSightseeingTransferModel.addSightseeingTransferData(service_id, admin_id, sightseeing_transfer_title, inclusions, pickup_point, drop_off_point, duration, sightseeing_transfer_description)

        # Send the Notification to the Dashboard
        flash('Sightseeing Transfer Added', 'success')

        return redirect(url_for('sightseeingTransferDataCenter', country=country, destination=destination, trip_id=trip_id))

    return render_template(
        'admin/adminSightseeingTransferDataCenter.html',
        country = country,
        destination = destination,
        trip_id = trip_id,
        form=form,
        sightseeing_transfer_data=sightseeing_transfer_data
    )
