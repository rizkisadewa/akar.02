# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

# Import from Model
from project.models.adminServiceModel import adminServiceModel

# an object form Admin Model
adminServiceModel = adminServiceModel()

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

# Add Services Data Form Class
class AddServiceData(Form):
    name_of_service = StringField('Name of Service', [validators.Length(min=1, max=200)])
    slug = StringField('Slug(URL)', [validators.Length(min=1, max=50)])

# Choose the Country
@app.route('/admin/service-setting')
@is_logged_in
def serviceChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminServiceSelectCountry.html', country_data=country_data)

# Choose the Destination
@app.route('/admin/service-setting/<string:country>')
@is_logged_in
def serviceChooseDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminTripModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminTripModel.destinationFetchOne(country)

    return render_template(
    'admin/adminServiceSelectDestination.html',
    destination_data=destination_data,
    country_data_fetch_one=country_data_fetch_one)

# Service Setting
@app.route('/admin/service-setting/<string:country>/<string:destination>/<string:trip_id>', methods=['GET', 'POST'])
@is_logged_in
def serviceDataCenter(country, destination, trip_id):

    # Fit the Services Form Class
    form = AddServiceData(request.form)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Services
    service_data = adminServiceModel.serviceFetchData(destination)

    # Fetch Trip DAta
    # Add the Data
    if request.method == 'POST' and form.validate():
        name_of_service = form.name_of_service.data
        trip_id = trip_data['trip_id']
        slug = form.slug.data

        adminServiceModel.addServiceData(name_of_service, trip_id, slug)

        flash('Service Added', 'success')

        return redirect(url_for('serviceDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminServiceDataCenter.html',
        trip_data=trip_data,
        service_data=service_data,
        destination=destination,
        country=country,
        form=form)


# Delete Service

@app.route('/admin/service-setting/<string:country>/<string:destination>/<string:trip_id>/<string:service_id>/delete', methods=['GET', 'POST'])
@is_logged_in
def serviceDataDelete(country, destination, trip_id, service_id):

    # Execute Query in Model
    adminServiceModel.serviceDataDelete(service_id)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # show notification
    flash('Service Data Deleted', 'danger')

    return redirect(url_for('serviceDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))
