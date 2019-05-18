# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField
from functools import wraps

# Import from Model
from project.models.adminPackageTripModel import adminPackageTripModel
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel
from project.models.adminDayExcursionModel import adminDayExcursionModel

# an object from admin model
adminPackageTripModel = adminPackageTripModel()
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()
adminDayExcursionModel = adminDayExcursionModel()


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


# Add Component of Package Trip Form Class
class AddComponentPackageTripData(Form):
    day_no = IntegerField(u'Day No :')


# Add Day Excursion to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion', methods=['GET','POST'])
@is_logged_in
def componentPackageTripAddDayExcursion(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Day Excursion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionDataFetchOneServiceId(package_trip_data['service_id'])

    # Add the Data
    if request.method == 'POST' and form.validate():
        day_no = form.day_no.data
        day_excursion_id = day_excursion_data[0]['day_excursion_id']

        # Execute Query : add the data
        adminPackageTripModel.addPackageTripComponent(day_excursion_id, package_trip_id, day_no)

        # send notification
        flash('Package Trip Component Added', 'success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripAddDayExcursion.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        day_excursion_data=day_excursion_data)

# Edit Day Excursion Day No
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion/edit/<string:tr_package_trip_day_excursion_id>', methods=['POST', 'GET'])
@is_logged_in
def componentPackageTripEditDayExcursion(country, destination, trip_id, package_trip_id, tr_package_trip_day_excursion_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Day Excursion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionDataFetchOneServiceId(package_trip_data['service_id'])

    # Fetch Package Trip Component
    component_data = adminPackageTripModel.packageTripComponentDataFetchOne(package_trip_id, tr_package_trip_day_excursion_id)

    # Populate Package Trip Component from fields
    form.day_no.data = component_data['day_no']

    # Update Package Trip Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        day_no = request.form['day_no']

        # Execute the query
        adminPackageTripModel.packageTripComponentUpdateData(day_no, tr_package_trip_day_excursion_id)

        # Send notification to the dashboard
        flash('Package Trip Compnent has been updated', 'success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripEditDayExcursion.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        day_excursion_data=day_excursion_data,
        component_data=component_data)

# Delete the Day Excursion from Package Trip
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion/delete/<string:tr_package_trip_day_excursion_id>',methods=['GET','POST'])
@is_logged_in
def componentPackageTripDeleteDayExcursion(country, destination, trip_id, package_trip_id, tr_package_trip_day_excursion_id):

    # Execute query from the model
    adminPackageTripModel.deletePackageTripComponentData(tr_package_trip_day_excursion_id)


    # Send notification to the dashboard
    flash('Package Trip Compnent has been deleted', 'danger')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
