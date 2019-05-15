# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, IntegerField, FloatField
from functools import wraps
import sys
import os

# Declaring the APP_ROOT
APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))

# os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))
# os.path.dirname(os.path.abspath(__file__))

# Import from Model
from project.models.adminServiceModel import adminServiceModel
from project.models.adminPackageExcursionModel import adminPackageExcursionModel
from project.models.adminServiceDetailModel import adminServiceDetailModel
from project.models.adminTripModel import adminTripModel

# an object form Admin Model
adminServiceModel = adminServiceModel()
adminPackageExcrusionModel = adminPackageExcursionModel()
adminServiceDetailModel = adminServiceDetailModel()
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
class AddServiceDetailData(Form):
    day_no = IntegerField(u'Day No :')
    package_title = StringField()


# Service Component Datails
@app.route('/admin/services-data-center/<string:destination>/component-details/<string:service_id>', methods=['GET', 'POST'])
@is_logged_in
def serviceDataComponentDetails(destination, service_id):

    # Fetch one trip data refer to the destination
    service_trip_data = adminServiceModel.serviceTripFetchData(destination)

    #Fetch One Service Data
    service_data = adminServiceModel.serviceDataFetchOne(service_id)
    #Fetch Data Trip id refer to Destination
    trip_id = adminTripModel.tripIdFetchOneFromDestination(destination)
    # Fetch Data of Package Excursion Data
    package_excursion_data = adminPackageExcrusionModel.packageExcrusionDataFetchFromTripId(trip_id['trip_id'])
    # Fetch Data of Service Detail Data
    service_detail_data = adminServiceDetailModel.serviceDetailFetchData(service_id)
    # Fetch Data of Service Image Data
    service_image_data = adminServiceDetailModel.serviceImageDataFetch(service_id)

    # Fetch Image Profile
    service_image_profile = adminServiceDetailModel.serviceImageProfileDataFetch(service_data['file_name'])

    # Testing Last Service Image Id
    last_srv_img_id = adminServiceDetailModel.lastServiceImageId()

    # Fit the Services Form Class
    form = AddServiceDetailData(request.form)

    # Add the Data
    if request.method == 'POST' and form.validate():
        day_no = form.day_no.data
        package_title = form.package_title.data
        package_excursion_id = adminServiceDetailModel.packageExcursionIdFetchOne(package_title) # search the package excursion id refer to package_title

        # Execute Query : add the data
        adminServiceDetailModel.addServiceDetailData(day_no, package_excursion_id["package_excursion_id"], package_title, service_id)


        flash('Service Component Added', 'success')

        return redirect('/admin/services-data-center/'+destination+'/component-details/'+service_id)

    return render_template('admin/serviceDetailData.html',
    service_data=service_data,
    package_excursion_data=package_excursion_data,
    service_detail_data=service_detail_data,
    form=form,
    service_image_data=service_image_data,
    service_trip_data=service_trip_data,
    service_image_profile=service_image_profile,
    last_srv_img_id=last_srv_img_id['MAX(service_image_id)'])

# Delete Service Details
@app.route('/admin/services-data-center/component-details/<string:destination>/delete/<string:service_detail_id>?<string:service_id>', methods=['GET', 'POST'])
@is_logged_in
def deleteServiceDetails(destination, service_detail_id, service_id):

    # execute query in model
    adminServiceDetailModel.deleteServiceDetailData(service_detail_id)

    # show flash message in dashboard
    flash('Service Detail Component ID '+service_detail_id+' Deleted', 'danger')

    return redirect('/admin/services-data-center/'+destination+'/component-details/'+service_id)

# Uploading the service images
@app.route('/admin/services-data-center/component-details/<string:destination>/image/<string:service_id>', methods=['GET', 'POST'])
@is_logged_in
def uploadServiceImage(destination, service_id):

    # make the target to folder
    target = os.path.join(APP_ROOT, 'static/images/services')

    # Checking the directory, if there is no directory, then we make it.
    if not os.path.isdir(target):
        os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))

    # Service Image Id Triger
    adminServiceDetailModel.addServiceImageData(target)
    last_srv_img_id = adminServiceDetailModel.lastServiceImageId()

    # uploading the file
    for file in request.files.getlist("file"):
        
        file_name = "-".join([destination, file.filename])
        file_name = "-".join([str(last_srv_img_id['MAX(service_image_id)']), file_name])
        path = "/".join([target, file_name])
        file.save(path)

    # make the target and path special for DB
    db_target = 'static/images/services'
    db_path = "/".join([db_target, file_name])

    # updating the service image data
    adminServiceDetailModel.editServiceImageData(service_id, file_name, db_path, last_srv_img_id['MAX(service_image_id)'])

    # showing the notification to the dashboard
    flash("Image has been added", 'success')

    return redirect('/admin/services-data-center/'+destination+'/component-details/'+service_id)

# Deleting the service image
@app.route('/admin/services-data-center/component-details/<string:destination>/image/delete/<string:service_id>?<string:service_image_id>?<string:file_name>', methods=['GET', 'POST'])
@is_logged_in
def deleteServiceImage(destination, service_id, service_image_id, file_name):

    # -- DELETING THE FILE ---
    # make the target to folder
    target = os.path.join(APP_ROOT, 'static/images/services')

    # set the service image id into null in services to avoid delete the service data
    adminServiceModel.setServiceImageIdNull(service_id)

    # deleting the file
    path = "/".join([target, file_name])
    os.remove(path)

    # -- DELETING THE DATABASE ---
    # Execute the query from the model
    adminServiceDetailModel.deleteServiceImageData(service_image_id)

    # showing the notification on the dashboard
    flash('Service Image has been deleted', 'danger')

    return redirect('/admin/services-data-center/'+destination+'/component-details/'+service_id)

# Set Service Image Profile
@app.route('/admin/services-data-center/component/<string:destination>/image/set-profile<string:service_id>?<string:service_image_id>?<string:file_name>', methods=['GET', 'POST'])
@is_logged_in
def setServiceImageProfile(destination, service_id, service_image_id, file_name):

    # Execute query for service Service Image Profile
    adminServiceDetailModel.setServiceImageProfile(service_image_id, service_id, file_name)

    # showing the notification on the dashboard
    flash('Service Image has been set as Service Image Profile', 'success')

    return redirect('/admin/services-data-center/'+destination+'/component-details/'+service_id)
