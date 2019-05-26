# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField, SelectMultipleField
from functools import wraps
import sys
import os


# Declaring the APP_ROOT
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))

# Import from Model
from project.models.adminPackageTripModel import adminPackageTripModel
from project.models.adminTripModel import adminTripModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminModels import adminModel
from project.models.adminDayExcursionModel import adminDayExcursionModel
from project.models.adminItineraryModel import adminItineraryModel
from project.models.adminRateCardModel import adminRateCardModel

# an object from admin model
adminPackageTripModel = adminPackageTripModel()
adminTripModel = adminTripModel()
adminServiceModel = adminServiceModel()
adminModel = adminModel()
adminDayExcursionModel = adminDayExcursionModel()
adminItineraryModel = adminItineraryModel()
adminRateCardModel = adminRateCardModel()

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

# Add Rate Card Data Form Class
class AddRateCardData(Form):
    package_trip_id = IntegerField()
    name_of_hotel = StringField()
    name_of_rate = StringField()

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

    # Fetch Package Trip Data
    package_trip_data = adminPackageTripModel.packageTripFetchData(trip_id, destination)

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Add the Data
    if request.method == 'POST' and form.validate():
        service_id = service_data['service_id']
        admin_id = admin_data['admin_id']
        package_trip_name = form.package_trip_name.data
        validity_date_start = form.validity_date_start.data
        validity_date_finish = form.validity_date_finish.data
        tag_line = form.tag_line.data
        inclusions = form.inclusions.data

        # Execute Query
        adminPackageTripModel.addPackageTrip(service_id, admin_id, package_trip_name, validity_date_start, validity_date_finish, tag_line, inclusions)

        flash('Package Added', 'success')

        return redirect(url_for('packageTripDataCenter', country=trip_data['country'], destination=trip_data['destination'], trip_id=trip_data['trip_id']))

    return render_template(
        'admin/adminPackageTripDataCenter.html',
        trip_data=trip_data,
        destination=destination,
        country=country,
        service_data=service_data,
        package_trip_data=package_trip_data,
        form=form
    )

# Package Trip Data Update
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/edit/<string:package_trip_id>', methods=['GET', 'POST'])
@is_logged_in
def packageTripDataEdit(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fetch Trip Data
    trip_data = adminTripModel.tripDataFetchOne(trip_id)

    # Fit the Package Trip Form Class
    form = AddPackageTripData(request.form)

    # Populate Package Trip from fields
    form.package_trip_name.data = package_trip_data['package_trip_name']
    form.tag_line.data = package_trip_data['tag_line']
    form.validity_date_start.data = package_trip_data['validity_date_start']
    form.validity_date_finish.data = package_trip_data['validity_date_finish']
    form.inclusions.data = package_trip_data['inclusions']

    # Update Package Trip Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        package_trip_name = request.form['package_trip_name']
        tag_line = request.form['tag_line']
        validity_date_start = request.form['validity_date_start']
        validity_date_finish = request.form['validity_date_finish']
        inclusions = request.form['inclusions']

        # Execute the query
        adminPackageTripModel.updatePackageTripData(package_trip_name, tag_line, validity_date_start, validity_date_finish, inclusions, package_trip_id)

        # Send notification to the dashboard
        flash('Package Trip has been updated', 'success')

        return redirect(url_for('packageTripDataCenter', country=country, destination=destination, trip_id=trip_id))

    return render_template('admin/adminPackageTripDataEdit.html',
    form=form,
    trip_data=trip_data,
    country=country,
    destination=destination,
    package_trip_data=package_trip_data)

# Delete Package Trip Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/delete/<string:package_trip_id>', methods=['GET', 'POST'])
@is_logged_in
def deletePackageTripData(country, destination, trip_id, package_trip_id):

    # Execute query from the model
    adminPackageTripModel.deletePackageTripData(package_trip_id)

    # Send Notification to the dashboard
    flash('Package Trip has been deleted', 'danger')

    return redirect(url_for('packageTripDataCenter', country=country, destination=destination, trip_id=trip_id))

# Package Trip Data Component Detail
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>', methods=['GET','POST'])
@is_logged_in
def componentPackageTrip(country, destination, trip_id, package_trip_id):

    # Fetch One Package Trip Data from package_trip_id
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Fitting the Form Add Rate Card Data
    form = AddRateCardData(request.form)

    # Fetch the Day Excursion Data
    day_excursion_data = adminDayExcursionModel.dayExcursionDataFetchOneServiceId(package_trip_data['service_id'])

    # Component Data
    component_data = adminItineraryModel.itineraryFetchData(package_trip_id)

    # Fetch Image Data - Package Trip
    package_trip_image_data = adminPackageTripModel.packageTripImageDataFetch(package_trip_id)

    # Feth Package Trip Image Profie
    package_trip_image_profile = adminPackageTripModel.packageTripImageProfile(package_trip_data['package_trip_image_profile'])

    # Fetch Rate Card
    rate_card_data = adminRateCardModel.rateCardDataFetchAll(package_trip_id)

    return render_template(
        'admin/adminPackageTripComponent.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        package_trip_data=package_trip_data,
        day_excursion_data=day_excursion_data,
        component_data=component_data,
        package_trip_image_data=package_trip_image_data,
        package_trip_image_profile=package_trip_image_profile,
        form=form,
        rate_card_data=rate_card_data
        )

# Uploading the service images
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/add-image', methods=['GET','POST'])
@is_logged_in
def uploadPackageTripImage(country, destination, trip_id, package_trip_id):

    # make the target to folder
    target = os.path.join(APP_ROOT, 'static/images/package_trip')

    # Checking the directory, if there is no directory, then we make it.
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    # Service Image Id Triger
    adminPackageTripModel.addPackageTripImageData(target)
    last_srv_img_id = adminPackageTripModel.lastPackageTripImageId()

    # uploading the file
    for file in request.files.getlist("file"):

        # manipulate the file name
        file_name = "-".join([destination, file.filename])
        file_name = "-".join([str(last_srv_img_id['MAX(package_trip_image_id)']), file_name])
        path = "/".join([target, file_name])

        # save the image to the folder
        file.save(path)

    # make the target and path special for DB
    db_target = 'static/images/package_trip'
    db_path = "/".join([db_target, file_name])

    # Updating the Package Trip Image Data
    adminPackageTripModel.editPackageTripImageData(package_trip_id, file_name, db_path, last_srv_img_id['MAX(package_trip_image_id)'])

    # Send notification to the dashboard
    flash("Image has been added", 'success')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

# Deleting the Package Trip Image Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/delete-image/<string:package_trip_image_id>?<string:file_name>', methods=['GET','POST'])
@is_logged_in
def deletePackageTripImage(country, destination, trip_id, package_trip_id, package_trip_image_id, file_name):
    # -- DELETING THE FILE ---
    # make the target to folder
    target = os.path.join(APP_ROOT, 'static/images/package_trip')

    # Fetch One Package Trip
    package_trip_data = adminPackageTripModel.packageTripDataFetchOne(package_trip_id)

    # Checking the Package Trip Image Profile
    if package_trip_data['package_trip_image_profile'] == package_trip_image_id:
        # Set package trip image profile to null
        adminPackageTripModel.setPackageTripImageProfileNull(package_trip_id)

    # deleting the file
    path = "/".join([target, file_name])
    os.remove(path)

    # -- DELETING THE DATABASE ---
    # Execute the query from the model
    adminPackageTripModel.deletePackageTripImage(package_trip_image_id)

    # showing the notification on the dashboard
    flash('Package Trip Image has been deleted', 'danger')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

# Setting the Package Trip Image Profile Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/set-profile/<string:package_trip_image_id>?<string:file_name>', methods=['GET', 'POST'])
@is_logged_in
def setPackageTripImageProfile(country, destination, trip_id, package_trip_id, package_trip_image_id, file_name):

    # Exe Cute query for setting Package Trip Image Profile
    adminPackageTripModel.setPackageTripImageProfile(package_trip_image_id, package_trip_id)

    # showing the notification to the dashboard
    flash('Package Image Profile has been set up', 'success')

    return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
