# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField
from functools import wraps

#import from Model
from project.models.adminDayExcursionModel import adminDayExcursionModel
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel

# an object from Admin Models
adminDayExcursionModel = adminDayExcursionModel()
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

# Add Day Excursion Data Form Class
class AddDayExcursionData(Form):
    day_excursion_title = StringField('Day Excursion Title', [validators.Length(min=1, max=200)])
    day_excursions_description = TextAreaField(u'Day Excursion Description')
    inclusions = StringField(u'Day Excursion Inclusions')
    estimation_time_start = TimeField(u'Estimation Time Start')
    estimation_time_finish = TimeField(u'Estimation Time Finish')

# Choose the Country
@app.route('/admin/day-excursion-setting')
@is_logged_in
def dayExcursionChooseCountry():

    # Fetch the Country Data
    country_data = adminTripModel.countryFetchData()

    return render_template('admin/adminDayExcursionSelectCountry.html', country_data=country_data)

# Choose the Destination
@app.route('/admin/day-excursion-setting/<string:country>')
@is_logged_in
def dayExcursionChooseDestination(country):

    # Fetch One Country Data
    country_data_fetch_one = adminTripModel.countryFetchOneData(country)

    # Fetch Destination Data
    destination_data = adminTripModel.destinationFetchOne(country)

    return render_template(
    'admin/adminDayExcursionSelectDestination.html',
    destination_data=destination_data,
    country_data_fetch_one=country_data_fetch_one)

# Day Excursion Setting
@app.route('/admin/day-excursion-setting/<string:country>/<string:destination>/<string:trip_id>', methods=['GET','POST'])
@is_logged_in
def dayExcursionDataCenter(country, destination, trip_id):

    form = AddDayExcursionData(request.form)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fetch Service Data
    service_data = adminServiceModel.serviceDataFetchOne(trip_id)

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Fetch Day Excrusion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionFetchData()

    # Add the Data
    if request.method == 'POST' and form.validate():
        service_id = service_data['service_id']
        admin_id = admin_data['admin_id']
        day_excursion_title = form.day_excursion_title.data
        day_excursions_description = form.day_excursions_description.data
        inclusions = form.inclusions.data
        estimation_time_start = form.estimation_time_start.data
        estimation_time_finish = form.estimation_time_finish.data

        # Execute Query
        adminDayExcursionModel.addDayExcursionData(service_id, admin_id, day_excursion_title, day_excursions_description, inclusions, estimation_time_start, estimation_time_finish)

        # Send Notification
        flash('Day Excursion Added', 'success')

        return redirect(url_for('dayExcursionDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminDayExcursionDataCenter.html',
        form=form,
        trip_data=trip_data,
        destination=destination,
        country=country,
        service_data=service_data,
        day_excursion_data=day_excursion_data
    )

# Day Excursion Update Data
@app.route('/admin/day-excursion-setting/<string:country>/<string:destination>/<string:trip_id>/edit/<string:day_excursion_id>', methods=['GET','POST'])
@is_logged_in
def dayExcursionDataUpdate(country, destination, trip_id, day_excursion_id):

    # Fetch One Day Excursion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionDataFetchOne(day_excursion_id)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fit the Package Trip Form Class
    form = AddDayExcursionData(request.form)

    # Populate Package Trip from fields
    form.day_excursion_title.data = day_excursion_data['day_excursion_title']
    form.inclusions.data = day_excursion_data['inclusions']
    form.estimation_time_start.data = day_excursion_data['estimation_time_start']
    form.estimation_time_finish.data = day_excursion_data['estimation_time_finish']
    form.day_excursions_description.data = day_excursion_data['day_excursions_description']

    # Update Day Excursion Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        day_excursion_title = request.form['day_excursion_title']
        inclusions = request.form['inclusions']
        estimation_time_start = request.form['estimation_time_start']
        estimation_time_finish = request.form['estimation_time_finish']
        day_excursions_description = request.form['day_excursions_description']

        # Execute the query
        adminDayExcursionModel.updateDayExcursionData(day_excursion_title, inclusions, estimation_time_start, estimation_time_finish, day_excursions_description, day_excursion_id)

        # send notification to the dashboard
        flash('Day Excursion has been updated', 'success')

        return redirect(url_for('dayExcursionDataCenter', country=country, destination=destination, trip_id=trip_id))

    return render_template(
        'admin/adminDayExcursionEdit.html',
        form=form,
        destination=destination,
        country=country,
        trip_data=trip_data
    )
