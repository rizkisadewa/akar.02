# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps


#import from Model
from project.models.adminTripModel import adminTripModel

# an object from Admin Models
adminModel = adminTripModel()

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


# Add Trip Data Form Class
class AddTripData(Form):
    destination = StringField('Destination', [validators.Length(min=1, max=100)])
    country = StringField('Country', [validators.Length(min=1, max=100)])

# Trip Data Center
@app.route('/admin/trip-data-center', methods=['GET', 'POST'])
@is_logged_in
def tripDataCenter():

    #Fetch Data of Vendor Data
    trip_datas = adminModel.tripFetchData()
    trip_data = adminModel.tripFetchData()

    form = AddTripData(request.form)
    if request.method == 'POST' and form.validate():
        destination = form.destination.data
        country = form.country.data

        adminModel.addTripData(destination, country)

        flash('Trip Added', 'success')

        return redirect(url_for('tripDataCenter'))
    return render_template(
        'admin/tripData.html',
        form=form,
        trip_datas=trip_datas,
        trip_data=trip_data)

# Trip Data Update
@app.route('/admin/trip-data-center/edit/<string:trip_id>', methods=['GET', 'POST'])
@is_logged_in
def tripDataEdit(trip_id):

    #Fetch One Trip Data
    trip_data = adminModel.tripDataFetchOne(trip_id)

    # Fit the Trip Form Class
    form = AddTripData(request.form)

    # Populate Trip from fields
    form.destination.data = trip_data['destination']
    form.country.data = trip_data['country']

    # Update Trip Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        destination = request.form['destination']
        country = request.form['country']

        # Execute the query
        adminModel.updateTripData(destination, country, trip_id)

        flash('Trip ID '+trip_id+' Updated', 'success')

        return redirect(url_for('tripDataCenter'))

    return render_template('admin/tripDataEdit.html', form=form)

# Trip Data Delete
@app.route('/admin/trip-data-center/delete/<string:trip_id>', methods=['POST'])
@is_logged_in
def deleteTripData(trip_id):
    adminModel.deleteTripData(trip_id)

    flash('Trip ID '+trip_id+' Deleted', 'danger')

    return redirect(url_for('tripDataCenter'))

# Select Country
@app.route('/admin/select-country')
@is_logged_in
def selectCountry():

    # Fetch the Country Data
    country_data = adminModel.countryFetchData()

    # Fetch the Trip Data
    trip_data = adminModel.tripFetchData()

    return render_template('admin/selectCountry.html', country_data=country_data)

@app.route('/admin/select-country/select-destination/<string:country>')
@is_logged_in
def selectDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminModel.destinationFetchOne(country)

    return render_template(
    'admin/selectDestination.html',
    destination_data=destination_data,
    country_data_fetch_one=country_data_fetch_one,
    trip_data=trip_data)
