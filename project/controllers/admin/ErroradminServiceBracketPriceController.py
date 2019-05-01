# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, FloatField, TimeField, IntegerField, DecimalField
from functools import wraps

# Import from Model
from project.models.adminPriceSegmentModel import adminPriceSegmentModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminServiceBracketPriceModel import adminServiceBracketPriceModel

# an object from Admin Model
adminPriceSegmentModel = adminPriceSegmentModel()
adminServiceModel = adminServiceModel()
adminServiceBracketPriceModel = adminServiceBracketPriceModel()

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

# Add Pax Bracket Price Form Class
class AddPaxBracketPrice(Form):
    min_pax = IntegerField(u'Minimum Pax')
    max_pax = IntegerField(u'Maximum Pax')
    price_per_person = FloatField(u'Price Per Person')
    segment_type = StringField()

# Add Service Bracket Price
@app.route('/admin/services-data-center/service-bracket-price/<string:service_id>', methods=['GET','POST'])
@is_logged_in
def serviceBracketPriceDataCenter(service_id):

    # Fit the Service Bracket Price Form Class
    form = AddPaxBracketPrice(request.form)

    # Fetch Price Segment Data
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    #Fetch One Service Data
    service_data = adminServiceModel.serviceDataFetchOne(service_id)

    # Fetch All Service Bracket Price
    service_bracket_price_data = adminServiceBracketPriceModel.serviceBracketPriceFetchData(service_id)

    # Add the data
    if request.method == 'POST' and form.validate():
        min_pax = form.min_pax.data
        max_pax = form.max_pax.data
        price_per_person = form.price_per_person.data
        segment_type = form.segment_type.data
        # Fetch Price Segment ID refer to the segment_type input in the form
        price_segment_id = adminServiceBracketPriceModel.priceSegmentIdFetchOne(segment_type)

        # Execute query : ad the data into the database
        adminServiceBracketPriceModel.addServiceBracketPrice(min_pax, max_pax, price_per_person, service_id, price_segment_id["price_segment_id"])

        # Showing the notification to the dashboard
        flash('Service Bracket Price has been updated', 'success')

        # redirect to the same url
        return redirect('/admin/services-data-center/service-bracket-price/'+service_id)

    return render_template('admin/serviceBracketPrice.html',
    price_segment_data=price_segment_data,
    service_data=service_data,
    form=form,
    service_bracket_price_data=service_bracket_price_data)

# Delete Service Bracket Price
@app.route('/admin/services-data-center/service-bracket-price/delete/<string:service_id>?<string:service_bracket_price_id>', methods=['GET', 'POST'])
@is_logged_in
def deleteServiceBracketPrice(service_id, service_bracket_price_id):

    # Execute the query in model
    adminServiceBracketPriceModel.deleteServiceBracketPrice(service_bracket_price_id)

    # show notification on the dashboard
    flash('Service Bracket ID '+service_bracket_price_id+' has been deleted', 'danger')

    # redirect to the same url
    return redirect('/admin/services-data-center/service-bracket-price/'+service_id)
