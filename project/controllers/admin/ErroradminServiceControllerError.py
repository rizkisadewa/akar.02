# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField
from functools import wraps

# Import from Model
from project.models.adminServiceModel import adminServiceModel
from project.models.adminTripModel import adminTripModel

# an object form Admin Model
adminModel = adminServiceModel()
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
    name_of_service = StringField('Name of Services', [validators.Length(min=1, max=200)])
    validity_date_start = DateField('Validity Date Start', format='%Y-%m-%d')
    validity_date_finish = DateField('Validity Date Finish', format='%Y-%m-%d')
    tag_line = StringField('Tag Line', [validators.Length(min=1, max=200)])
    inclusions = TextAreaField('Inclusions', [validators.Length(min=1, max=500)])

# Service Data Center And Adding Data
@app.route('/admin/services-data-center/<string:destination>', methods=['GET', 'POST'])
@is_logged_in
def servicesDataCenter(destination):

    # Fetch Data of Service Data
    service_trip_data = adminModel.serviceTripFetchData(destination)
    trip_data = adminTripModel.tripFetchData()
    services_data = adminModel.serviceFetchData(service_trip_data['trip_id'])

    # Fit the Services Form Class
    form = AddServiceData(request.form)

    # Add the Data
    if request.method == 'POST' and form.validate():
        name_of_service = form.name_of_service.data
        trip_id = service_trip_data['trip_id']
        validity_date_start = form.validity_date_start.data
        validity_date_finish = form.validity_date_finish.data
        tag_line = form.tag_line.data
        inclusions = form.inclusions.data

        adminModel.addServiceData(name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions)

        flash('Service Added', 'success')

        return redirect(url_for('servicesDataCenter', destination=service_trip_data['destination']))

    return render_template('admin/servicesData.html',
    form=form,
    services_data=services_data,
    trip_data=trip_data,
    service_trip_data=service_trip_data)

# Delete Service Data
@app.route('/admin/services-data-center/<string:destination>/delete/<string:service_id>', methods=['POST'])
@is_logged_in
def deleteServiceData(destination, service_id):

    service_trip_data = adminModel.serviceTripFetchData(destination)

    adminModel.deleteServiceData(service_id)
    flash('Service ID '+service_id+' Deleted', 'danger')

    return redirect(url_for('servicesDataCenter', destination=service_trip_data['destination']))

# Update Service Data
@app.route('/admin/services-data-center/<string:destination>/edit/<string:service_id>', methods=['GET','POST'])
@is_logged_in
def serviceDataEdit(destination, service_id):

    #Fetch One Service Data
    service_data = adminModel.serviceDataFetchOne(service_id)
    # Fetch Data of Service Data
    service_trip_data = adminModel.serviceTripFetchData(destination)

    # Fetch All Trip Data
    trip_data = adminTripModel.tripFetchData()

    # Fit the Service Data Form Class
    form = AddServiceData(request.form)

    # Populate Service Data from fields
    form.name_of_service.data = service_data['name_of_service']
    form.validity_date_start.data = service_data['validity_date_start']
    form.validity_date_finish.data = service_data['validity_date_finish']
    form.tag_line.data = service_data['tag_line']
    form.inclusions.data = service_data['inclusions']

    # Update Service Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        name_of_service = request.form['name_of_service']
        trip_id = service_trip_data['trip_id']
        validity_date_start = request.form['validity_date_start']
        validity_date_finish = request.form['validity_date_finish']
        tag_line = request.form['tag_line']
        inclusions = request.form['inclusions']

        # Execute the query
        adminModel.updateServiceData(name_of_service, trip_id, validity_date_start, validity_date_finish, tag_line, inclusions, service_id)

        flash('Service ID '+service_id+' Updated', 'success')

        return redirect(url_for('servicesDataCenter', destination=service_trip_data['destination']))

    return render_template('admin/serviceDataEdit.html', form=form, trip_data=trip_data, service_data=service_data)
