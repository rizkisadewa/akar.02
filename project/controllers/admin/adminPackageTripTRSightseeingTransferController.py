# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField
from functools import wraps

# Import from Model
from project.models.adminPackageTripModel import adminPackageTripModel
from project.models.adminSightseeingTransferModel import adminSightseeingTransferModel
from project.models.adminItineraryModel import adminItineraryModel
from project.models.adminPackageTripTRSightseeingTransferModel import adminPackageTripTRSightseeingTransferModel

# an object from admin model
adminPackageTripModel = adminPackageTripModel()
adminSightseeingTransferModel = adminSightseeingTransferModel()
adminItineraryModel = adminItineraryModel()
adminPackageTripTRSightseeingTransferModel = adminPackageTripTRSightseeingTransferModel()

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

# Add Component(Sightseeing Transfer) of Package Trip Form Class
class AddComponentPackageTripData(Form):
    day_no = IntegerField(u'Day No :')
    sightseeing_transfer_id = IntegerField()

# Add Sightseeing Transfer to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/sightseeing-transfer', methods=['GET','POST'])
@is_logged_in
def componentPackageTripAddSightseeingTransfer(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fit the Add Component of Package Trip Form Class
    form = AddComponentPackageTripData(request.form)

    # FEtch the Sightseeing Transfer Data
    sightseeing_transfer_data = adminSightseeingTransferModel.sightseeingTransferFetchData(trip_id)

    # Add the Data
    if request.method == 'POST' and form.validate():
        day_no = form.day_no.data
        sightseeing_transfer_id = form.sightseeing_transfer_id.data

        # Fetch One the sightseeing_transfer refer to sightseeing_transfer_id
        sightseeing_transfer_fetch_one = adminSightseeingTransferModel.sightseeingTransferDataFetchOne(sightseeing_transfer_id)

        # Execute Query : add the itinerary
        adminItineraryModel.addItinerary(day_no, package_trip_id, sightseeing_transfer_fetch_one['sightseeing_transfer_title'], sightseeing_transfer_fetch_one['sightseeing_transfer_description'], "Sightseeing Transfer")

        # Fetch the Itinerary data
        itinerary_data = adminItineraryModel.lastUpdateItinerary()

        # Execute Query : add the data
        adminPackageTripTRSightseeingTransferModel.addPackageTripSightseeingTransferData(sightseeing_transfer_id, package_trip_id, day_no, itinerary_data['itinerary_id'])

        # Send notification
        flash('Sightseeing Transfer has been added as component', 'success')

        # redirect to the package trip component
        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    return render_template(
        'admin/adminPackageTripTRAddSightseeingTransfer.html',
        form=form,
        package_trip_data=package_trip_data,
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        sightseeing_transfer_data=sightseeing_transfer_data
    )

# Edit Sightseeing Transfer to Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/sightseeing-transfer/edit/<string:itinerary_id>', methods=['GET','POST'])
@is_logged_in
def componentPackageTripEditSightseeingTransfer(country, destination, trip_id, package_trip_id, itinerary_id):
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

        # asight the variable value from request form value
        day_no = request.form['day_no']

        # Execute query for update Day No of Itinerary Table
        adminItineraryModel.updateDayNo(day_no, itinerary_id)

        # Execute query for update Day No of Sightseeing Transfer Table
        adminPackageTripTRSightseeingTransferModel.updatePackageTripSightseeingTransferData(day_no, itinerary_id)

        # Send notification to the dashboard
        flash('Sightseeing Transfer in Itinerary has been updated', 'success')

        # redirect to the package trip component
        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))


    return render_template(
        'admin/adminPackageTripTREditSightseeingTransfer.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        form=form,
        itinerary_data=itinerary_data,
        package_trip_data=package_trip_data
    )

# Deleting Sightseeing Transfer to PackageTrip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/sightseeing-transfer/delete/<string:itinerary_id>', methods=['GET', 'POST'])
@is_logged_in
def componentPackageTripDeleteSightseeingTransfer(country, destination, trip_id, package_trip_id, itinerary_id):
    # Execute query for delete Itinerary Table
    adminItineraryModel.deleteItineraryData(itinerary_id)

    # Execute query for delete Sightseeing Transfer Transaction Table
    adminPackageTripTRSightseeingTransferModel.deletePackageTripSightseeingTransferData(itinerary_id)

    # Send notification to the dashboard
    flash('Sightseeing Transfer has been deleted from Itinerary', 'danger')

    # redirect to the package trip component
    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
