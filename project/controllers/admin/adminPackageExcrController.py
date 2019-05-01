# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, FloatField, TimeField
from functools import wraps
import time as t

# Import from Model
from project.models.adminPackageExcursionModel import adminPackageExcursionModel
from project.models.adminTripModel import adminTripModel


# an object form Admin Model
adminModel = adminPackageExcursionModel()
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
class AddPackageExcursionData(Form):
    package_title = StringField('Package Title', [validators.Length(min=1, max=100)])
    package_description = TextAreaField(u'Package Description')
    inclusions = StringField(u'Package Inclusions')
    estimation_time_start = TimeField(u'Estimation Time Start')
    estimation_time_finish = TimeField(u'Estimation Time Finish')
    trip_id = StringField()

@app.route('/admin/package-excursion', methods=['GET', 'POST'])
@is_logged_in
def packageExcusionDataCenter():

    # Fetch Data of Service Data
    package_excursion_data = adminModel.packageExcursionFetchData()
    trip_data = adminTripModel.tripFetchData()

    # Fit the Services Form Class
    form = AddPackageExcursionData(request.form)

    if request.method == 'POST' and form.validate():
        package_title = form.package_title.data
        package_description = form.package_description.data
        inclusions = form.inclusions.data
        estimation_time_start = form.estimation_time_start.data
        estimation_time_finish = form.estimation_time_finish.data
        trip_id = form.trip_id.data

        # execute query in model
        adminModel.addPackageExcursionData(package_title, package_description, inclusions, estimation_time_start, estimation_time_finish, trip_id)

        # show flash message in dashboard
        flash('Package Added', 'success')

        return redirect(url_for('packageExcusionDataCenter'))

    return render_template(
        '/admin/packageExcursion.html',
        package_excursion_data = package_excursion_data,
        form=form,
        trip_data=trip_data)


# Delete Package Excursion Data
@app.route('/admin/package-excursion/delete/<string:package_excursion_id>', methods=['POST'])
@is_logged_in
def deletePackageExcursionData(package_excursion_id):

    # execute query in model
    adminModel.deletePackageExcursionData(package_excursion_id)

    # show flash message in dashboard
    flash('Package Excursion ID '+package_excursion_id+' Deleted', 'danger')

    return redirect(url_for('packageExcusionDataCenter'))


# Update Package Excursion Data
@app.route('/admin/package-excursion/edit/<string:package_excursion_id>/<string:trip_id>', methods=['GET', 'POST'])
@is_logged_in
def packageExcursionDataEdit(package_excursion_id, trip_id):

    #Fetch One Vendor Data
    package_excursion_data = adminModel.packageExcursionDataFetchOne(package_excursion_id)
    trip_data = adminTripModel.tripFetchData()

    #Add The Vendor Data
    form = AddPackageExcursionData(request.form)

    # Populate article from fields
    form.package_title.data = package_excursion_data['package_title']
    form.package_description.data = package_excursion_data['package_description']
    form.estimation_time_start.data = package_excursion_data['estimation_time_start']
    form.estimation_time_finish.data = package_excursion_data['estimation_time_finish']
    form.inclusions.data = package_excursion_data['inclusions']
    destination = adminTripModel.destinationFetchOneFromTripId(trip_id)
    form.trip_id.data = package_excursion_data['trip_id']

    # Update Trip Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        package_title = request.form['package_title']
        package_description = request.form['package_description']
        estimation_time_start = request.form['estimation_time_start']
        estimation_time_finish = request.form['estimation_time_finish']
        inclusions = request.form['inclusions']
        trip_id = request.form['trip_id']

        # Execute the query
        adminModel.updatePackageExcursionData(package_title, package_description, inclusions, estimation_time_start, estimation_time_finish,trip_id, package_excursion_id)

        flash('Package Excursion ID '+package_title+' Updated', 'success')

        return redirect(url_for('packageExcusionDataCenter'))

    return render_template('admin/packageExcursionEdit.html',
    form=form,
    package_excursion_data=package_excursion_data,
    trip_data=trip_data,
    destination=destination)
