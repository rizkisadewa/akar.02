# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField
from functools import wraps

# Import from Model
from project.models.adminPackageTripModel import adminPackageTripModel
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel

# an object from admin model
adminPackageExcrusionModel = adminPackageTripModel()
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()

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

# Add Package Trip Form Class
class AddPackageTripData(Form):
    package_trip_name = StringField('Package Trip Name', [validators.Length(min=1, max=200)])
    validity_date_start = DateField('Validity Date Start', format='%Y-%m-%d')
    validity_date_finish = DateField('Validity Date Finish', format='%Y-%m-%d')
    tag_line = StringField('Tag Line', [validators.Length(min=1, max=200)])
    inclusions = TextAreaField('Inclusions', [validators.Length(min=1, max=500)])

# Choose the Country
@app.route('/admin/package-trip-setting')
@is_logged_in
def packageTripChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminPackageTripSelectCountry.html', country_data=country_data)

# Choose the Destination
@app.route('/admin/package-trip-setting/<string:country>')
@is_logged_in
def packageTripChooseDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminTripModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminTripModel.destinationFetchOne(country)

    return render_template(
        'admin/adminPackageTripSelectDestination.html',
        destination_data=destination_data,
        country_data_fetch_one=country_data_fetch_one,
    )

# Package Trip Data Center
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>', methods=['GET','POST'])
@is_logged_in
def packageTripDataCenter(country, destination, trip_id):

    # Fit the Package Trip Form Class
    form = AddPackageTripData(request.form)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Service Data
    service_data = adminServiceModel.serviceDataFetchOne(trip_id)

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Add the Data
    if request.method == 'POST' and form.validate():
        service_id = service_data['trip_id']
        admin_id = admin_data['admin_id']
        package_trip_name = form.package_trip_name.data
        validity_date_start = form.validity_date_start.data
        validity_date_finish = form.validity_date_finish.data
        tag_line = form.tag_line.data
        inclusions = form.inclusions.data

        adminPackageTripModel.addPackageTrip(service_id, admin_id, package_trip_name, validity_date_start, validity_date_finish, tag_line, inclusions)

        flash('Package Added', 'success')

        return redirect(url_for('packageTripDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminPackageTripDataCenter.html',
        trip_data=trip_data,
        destination=destination,
        country=country,
        service_data=service_data,
        form=form
    )
