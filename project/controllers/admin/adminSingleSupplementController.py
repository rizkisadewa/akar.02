# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField, IntegerField, FloatField
from functools import wraps

# Import from Model
from project.models.adminPriceSegmentModel import adminPriceSegmentModel
from project.models.adminModels import adminModel
from project.models.adminSingleSupplementModel import adminSingleSupplementModel

# an object from Model
adminPriceSegmentModel = adminPriceSegmentModel()
adminModel = adminModel()
adminSingleSupplementModel = adminSingleSupplementModel()

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

# Add Package Bracket Price Data Form Class
class AddSingleSupplementData(Form):
    min_pax = IntegerField()
    max_pax = IntegerField()
    price_per_person = FloatField()
    price_segment_id = IntegerField()
    rate_card_id = IntegerField()


# Single Supplement Data Center
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/single-supplement/<string:rate_card_id>',methods=['GET','POST'])
@is_logged_in
def singleSupplementDataCenter(country, destination, trip_id, package_trip_id, rate_card_id):

    # Fit the Package Bracket Price Form Class
    form = AddSingleSupplementData(request.form)

    # Fetch the Price Segment Data
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Fetch Single Supplement Data
    single_supplement_data = adminSingleSupplementModel.singleSupplementFetchData()

    # Add the Data
    if request.method == 'POST' and form.validate():
        admin_id = admin_data['admin_id']
        min_pax = form.min_pax.data
        max_pax = form.max_pax.data
        price_per_person = form.price_per_person.data
        price_segment_id = form.price_segment_id.data
        rate_card_id = rate_card_id

        # Execute the query
        adminSingleSupplementModel.addSingleSupplementData(price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id)

        # Send the notification
        flash('Single Supplement has been added','success')

        # Redirect
        return redirect(url_for('singleSupplementDataCenter', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id, rate_card_id=rate_card_id))

    return render_template(
        'admin/adminSingleSupplementDataCenter.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        form=form,
        price_segment_data=price_segment_data,
        single_supplement_data=single_supplement_data,
        rate_card_id=rate_card_id
    )

# Edit the Single Supplement Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/single-supplement/<string:rate_card_id>/edit/<string:single_supplement_id>', methods=['GET','POST'])
@is_logged_in
def editSingleSupplement(country, destination, trip_id, package_trip_id, rate_card_id, single_supplement_id):

    # Fit the Single Supplement Form class
    form = AddSingleSupplementData(request.form)

    # Fetch the Price Segment Data
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    # Fetch One Single Supplement Data
    single_supplement_data_fo = adminSingleSupplementModel.singleSupplementFetchOne(single_supplement_id)

    # Populate Single Supplement Form Fields
    form.min_pax.data = single_supplement_data_fo['min_pax']
    form.max_pax.data = single_supplement_data_fo['max_pax']
    form.price_per_person.data = single_supplement_data_fo['price_per_person']

    # Update Package Bracket Price
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        min_pax = request.form['min_pax']
        max_pax = request.form['max_pax']
        price_per_person = request.form['price_per_person']
        price_segment_id = request.form['price_segment_id']

        # Execute the query
        adminSingleSupplementModel.updateSingleSupplementData(min_pax, max_pax, price_per_person, price_segment_id, single_supplement_id)

        # Send the notification to the dashboard
        flash('Single Supplement has been updated', 'success')

        # Redirect
        return redirect(url_for('singleSupplementDataCenter', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id, rate_card_id=rate_card_id))

    return render_template(
        'admin/adminSingleSupplementDataCenterEdit.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        form=form,
        price_segment_data=price_segment_data,
        rate_card_id=rate_card_id,
        single_supplement_data_fo=single_supplement_data_fo
    )
