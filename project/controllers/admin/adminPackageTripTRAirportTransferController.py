# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField
from functools import wraps

# Import from Model
from project.models.adminPackageTripModel import adminPackageTripModel
from project.models.adminAirportTransferModel import adminAirportTransferModel
from project.models.adminPackageTripTRAirportTransferModel import adminPackageTripTRAirportTransferModel
from project.models.adminItineraryModel import adminItineraryModel

# an object from admin model
adminPackageTripModel = adminPackageTripModel()
adminAirportTransferModel = adminAirportTransferModel()
adminPackageTripTRAirportTransferModel = adminPackageTripTRAirportTransferModel()
adminItineraryModel = adminItineraryModel()

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
    airport_transfer_id = IntegerField()

# Add Airport Transfer to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/airport-transfer', methods=['GET','POST'])
@is_logged_in
def componentPackageTripAddAirportTransfer(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Airport Transfer Data
    airport_transfer_data = adminAirportTransferModel.airportTransferFetchData(trip_id)

    # Add the Data
    if request.method == 'POST' and form.validate():
        day_no = form.day_no.data
        airport_transfer_id = form.airport_transfer_id.data

        # Fetch One the airport_transfer_data
        airport_transfer_fetch_one = adminAirportTransferModel.airportTransferDataFetchOne(airport_transfer_id)

        # Execute Query : add the itinerary
        adminItineraryModel.addItinerary(day_no, package_trip_id, airport_transfer_fetch_one['airport_transfer_title'], airport_transfer_fetch_one['airport_transfer_description'], "Airport Transfer")

        # Fetch the Itinerary data
        itinerary_data = adminItineraryModel.lastUpdateItinerary()

        # Execute Query : add the data
        adminPackageTripTRAirportTransferModel.addPackageTripAirportTransferData(airport_transfer_id, package_trip_id, day_no, itinerary_data['itinerary_id'])

        # Send notification
        flash('Airport Transfer has been added as component', 'success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripTRAddAirportTransfer.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        airport_transfer_data=airport_transfer_data
    )

# Edit Airport Transfer to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/airport-transfer/edit<string:itinerary_id>', methods=['GET','POST'])
@is_logged_in
def componentPackageTripEditAirportTransfer(country, destination, trip_id, package_trip_id, itinerary_id):
    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # Fetch the Itinerary Data
    itinerary_data = adminItineraryModel.itineraryFetchDataFromId(itinerary_id)

    # Populate Itinerary Data from fields
    form.day_no.data = itinerary_data['day_no']

    # Update Day No
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        day_no = request.form['day_no']

        # Execute query for update Day No of Itinerary Table
        adminItineraryModel.updateDayNo(day_no, itinerary_id)

        # Execute query for update Day No of Airport Transfer Transaction Table
        adminPackageTripTRAirportTransferModel.updatePackageTripAirportTransferData(day_no, itinerary_id)

        # Send notification to the dashboard
        flash('Airport Transfer in Itinerary has been updated','success')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripTREditAirportTransfer.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        form=form,
        itinerary_data=itinerary_data
    )

# Delete Airport Transfer to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/airport-transfer/delete/<string:itinerary_id>', methods=['GET','POST'])
@is_logged_in
def componentPackageTripDeleteAirportTransfer(country, destination, trip_id, package_trip_id, itinerary_id):

    # Execute query for delete Itinerary Table
    adminItineraryModel.deleteItineraryData(itinerary_id)

    # Execute query for delete Airport Transfer Transaction Table
    adminPackageTripTRAirportTransferModel.deletePackageTripAirportTransferData(itinerary_id)

    # Send notification to the dashboard
    flash('Airport Transfer in Itinerary has been deleted','danger')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
