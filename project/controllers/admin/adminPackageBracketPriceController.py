# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField, IntegerField, FloatField
from functools import wraps

# Import from Model
from project.models.adminPriceSegmentModel import adminPriceSegmentModel
from project.models.adminModels import adminModel
from project.models.adminPackageBracketPriceModel import adminPackageBracketPriceModel

# an object from Model
adminPriceSegmentModel = adminPriceSegmentModel()
adminModel = adminModel()
adminPackageBracketPriceModel = adminPackageBracketPriceModel()

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
class AddPackageBracketPriceData(Form):
    min_pax = IntegerField()
    max_pax = IntegerField()
    price_per_person = FloatField()
    price_segment_id = IntegerField()
    rate_card_id = IntegerField()


# Package Bracket Price Data Center
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/package-bracket-price/<string:rate_card_id>', methods=['GET','POST'])
@is_logged_in
def packageBracketPrice(country, destination, trip_id, package_trip_id, rate_card_id):

    # Fit the Package Bracket Price Form Class
    form = AddPackageBracketPriceData(request.form)

    # Fetch the Price Segment Data
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    # Fetch admin_id
    admin_data = adminModel.adminIdFetchOne(session['username'])

    # Fetch Package Bracket Price
    package_bracket_price_data = adminPackageBracketPriceModel.packageBracketPriceDataFetchData()

    # Add the Data
    if request.method == 'POST' and form.validate():
        admin_id = admin_data['admin_id']
        min_pax = form.min_pax.data
        max_pax = form.max_pax.data
        price_per_person = form.price_per_person.data
        price_segment_id = form.price_segment_id.data
        rate_card_id = rate_card_id

        # Execute the query
        adminPackageBracketPriceModel.addPackageBracketPriceData(price_segment_id, admin_id, min_pax, max_pax, price_per_person, rate_card_id)

        # Send the notification
        flash('Package Bracket Price has been added', 'success')

        # Redirect to the package component
        return redirect(url_for('packageBracketPrice', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id, rate_card_id=rate_card_id))

    return render_template(
        'admin/adminPackageBracketPriceDataCenter.html',
        country=country,
        destination=destination,
        trip_id=trip_id,
        package_trip_id=package_trip_id,
        form=form,
        price_segment_data=price_segment_data,
        package_bracket_price_data=package_bracket_price_data
    )

# Package Bracket Price Data Center
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/package-bracket-price/<string:rate_card_id>/<string:package_bracket_price_id>/delete', methods=['GET','POST'])
@is_logged_in
def packageBracketPriceDelete(country, destination, trip_id, package_trip_id, rate_card_id, package_bracket_price_id):

    # Execute query in Model
    adminPackageBracketPriceModel.deletePackageBracketPrice(package_bracket_price_id)

    # show notification to the dashboard
    flash('Package Bracket Price has been deleted','danger')

    # Redirect to the package component
    return redirect(url_for('packageBracketPrice', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id, rate_card_id=rate_card_id))
