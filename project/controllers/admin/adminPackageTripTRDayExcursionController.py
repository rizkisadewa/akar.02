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
from project.models.adminItineraryModel import adminItineraryModel
from project.models.adminPackageTripTRDayExcursionModel import adminPackageTripTRDayExcursionModel

# an object from admin model
adminPackageTripModel = adminPackageTripModel()
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()
adminDayExcursionModel = adminDayExcursionModel()
adminItineraryModel = adminItineraryModel()
adminPackageTripTRDayExcursionModel = adminPackageTripTRDayExcursionModel()


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
    day_excursion_id = IntegerField()


# Add Day Excursion to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion', methods=['GET','POST'])
@is_logged_in
def componentPackageTripAddDayExcursion(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Day Excursion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionDataFetchOneServiceId(trip_id)

    # Add the Data
    if request.method == 'POST' and form.validate():
        day_no = form.day_no.data
        day_excursion_id = form.day_excursion_id.data

        # Fetch One the Day Excursion Data
        day_excursion_fetch_one = adminDayExcursionModel.dayExcursionDataFetchOne(day_excursion_id)

        # Execute query : ad the Itinerary
        adminItineraryModel.addItinerary(day_no, package_trip_id, day_excursion_fetch_one['day_excursion_title'], day_excursion_fetch_one['day_excursions_description'], "Day Excursion")

        # Fetch the Itinerary Data
        itinerary_data = adminItineraryModel.lastUpdateItinerary()

        # Execute Query : add the data
        adminPackageTripTRDayExcursionModel.addPackageTripDayExcursionData(day_excursion_id, package_trip_id, day_no, itinerary_data['itinerary_id'])

        # send notification
        flash('Package Trip Component Added', 'success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripTRAddDayExcursion.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        day_excursion_data=day_excursion_data)

# Edit Day Excursion Day No
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion/edit/<string:itinerary_id>', methods=['POST', 'GET'])
@is_logged_in
def componentPackageTripEditDayExcursion(country, destination, trip_id, package_trip_id, itinerary_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Itinerary Data
    itinerary_data = adminItineraryModel.itineraryFetchDataFromId(itinerary_id)

    # Populate Package Trip Component from fields
    form.day_no.data = itinerary_data['day_no']

    # Update Package Trip Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        day_no = request.form['day_no']

        # Execute query for update Day No of Itinerary Table
        adminItineraryModel.updateDayNo(day_no, itinerary_id)

        # Execute query for update Day No of Day Excursion Transaction
        adminPackageTripTRDayExcursionModel.updatePackageTripDayExcursionData(day_no, itinerary_id)

        # Send notification to the dashboard
        flash('Package Trip Compnent has been updated', 'success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripTREditDayExcursion.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        itinerary_data=itinerary_data
    )

# Delete the Day Excursion from Package Trip
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/day-excursion/delete/<string:itinerary_id>',methods=['GET','POST'])
@is_logged_in
def componentPackageTripDeleteDayExcursion(country, destination, trip_id, package_trip_id, itinerary_id):

    # Execute query for deleting Itinerary Table
    adminItineraryModel.deleteItineraryData(itinerary_id)

    # Execute query for deleting Day Excursion Transaction Table
    adminPackageTripTRDayExcursionModel.deletePackageTripDayExcursionData(itinerary_id)

    # Send notification to the dashboard
    flash('Package Trip Compnent has been deleted', 'danger')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
