# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField, IntegerField
from functools import wraps

# Import from Model
from project.models.adminRateCardModel import adminRateCardModel
from project.models.adminPackageBracketPriceModel import adminPackageBracketPriceModel

# an object from admin model
adminRateCardModel = adminRateCardModel()
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

# Add Rate Card Data Form Class
class AddRateCardData(Form):
    package_trip_id = IntegerField()
    name_of_rate = StringField()
    name_of_hotel = StringField()

# Add Rate Card
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/add-rate-card', methods=['GET','POST'])
@is_logged_in
def addRateCardComponent(country,destination,trip_id,package_trip_id):

    form = AddRateCardData(request.form)

    # Add the Data
    if request.method == 'POST' and form.validate():
        name_of_rate = form.name_of_rate.data

        # Checking the data to avoid the redudant data
        standard_chk = adminRateCardModel.countingRateCardData(package_trip_id, "Standard")
        deluxe_chk = adminRateCardModel.countingRateCardData(package_trip_id, "Deluxe")
        premium_chk = adminRateCardModel.countingRateCardData(package_trip_id, "Premium")


        if name_of_rate == "Standard":
            if int(standard_chk['COUNT(*)']) < 1:
                # Execute the query
                adminRateCardModel.addRateCardData(package_trip_id, name_of_rate)

                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added','success')

            else:
                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added before','danger')

        elif name_of_rate == "Deluxe":
            if int(deluxe_chk['COUNT(*)']) < 1:

                # Execute the query
                adminRateCardModel.addRateCardData(package_trip_id, name_of_rate)

                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added','success')

            else:
                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added before','danger')

        elif name_of_rate == "Premium":
            if int(premium_chk['COUNT(*)']) < 1:

                # Execute the query
                adminRateCardModel.addRateCardData(package_trip_id, name_of_rate)

                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added','success')

            else:
                # Send the notification
                flash('Rate Card '+name_of_rate+' Has been added before','danger')

        else:
            # Send the notification
            flash('Error, the category is neither Standard nor Deluxe nor Premium','danger')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

# Deleting the Rate Card Data
@app.route('/admin/package-trip-setting/<string:country>/<string:destination>/<string:trip_id>/component/<string:package_trip_id>/delete-rate-card/<string:rate_card_id>', methods=['GET','POST'])
@is_logged_in
def deleteRateCardComponent(country,destination,trip_id,package_trip_id,rate_card_id):

    rate_card_checker = adminPackageBracketPriceModel.chkPriceBracketPrice(rate_card_id)

    if int(rate_card_checker['COUNT(*)']) < 1:

        adminRateCardModel.deleteRateCardData(rate_card_id)

        flash('Rate Card Has been deleted','danger')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))

    else :
        flash('Cannot be deleted due to there is still Package Bracket Price in this Rate Card')

        return redirect(url_for('componentPackageTrip', country=country, destination=destination, trip_id=trip_id, package_trip_id=package_trip_id))
