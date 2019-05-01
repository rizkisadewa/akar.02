# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, FloatField, TimeField
from functools import wraps

# Import from Model
from project.models.adminPriceSegmentModel import adminPriceSegmentModel

# an object form Admin Model
adminPriceSegmentModel = adminPriceSegmentModel()

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

# Add Price Segment Data Form Class
class AddPriceSegmentData(Form):
    segment_type = StringField('Segment Type', [validators.Length(min=1, max=100)])
    validity_date_start = DateField(u'Validity Date Start', format='%Y-%m-%d')
    validity_date_finish = DateField(u'Validity Date Start', format='%Y-%m-%d')

@app.route('/admin/price-segment', methods=['GET', 'POST'])
@is_logged_in
def priceSegmentDataCenter():

    # Fetch Data of Price Segment
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    # Fit the Price Segment Form Class
    form = AddPriceSegmentData(request.form)

    if request.method == 'POST' and form.validate():
        segment_type = form.segment_type.data
        validity_date_start = form.validity_date_start.data
        validity_date_finish = form.validity_date_finish.data

        # Execute Query in Model
        adminPriceSegmentModel.addPriceSegmentData(segment_type, validity_date_start, validity_date_finish)

        # show flash message in dashboard that the data success input
        flash('Price Segment', 'success')

        return redirect(url_for('priceSegmentDataCenter'))

    return render_template('/admin/priceSegment.html', form=form, price_segment_data=price_segment_data)

# Deleting the Price Segment Data
@app.route('/admin/price-segment/delete/<string:price_segment_id>', methods=['POST'])
@is_logged_in
def priceSegmentDelete(price_segment_id):

    # Execute the query from the Model
    adminPriceSegmentModel.deletePriceSegmentData(price_segment_id)

    # showing the notification on the dashboard
    flash('Price Segment ID '+price_segment_id+" Deleted", 'danger')

    # redirect to the Price Segment Data Center
    return redirect(url_for('priceSegmentDataCenter'))

# Updating the Price Segment Data
@app.route('/admin/price-segment/edit/<string:price_segment_id>', methods=['GET','POST'])
@is_logged_in
def priceSegmentDataEdit(price_segment_id):

    # Fetch One Price Segment
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchOne(price_segment_id)

    # Fit the Price Segment Form Class
    form = AddPriceSegmentData(request.form)

    # Populate Price Segment Data from fields
    form.segment_type.data = price_segment_data['segment_type']
    form.validity_date_start.data = price_segment_data['validity_date_start']
    form.validity_date_finish.data = price_segment_data['validity_date_finish']

    # Update the Price Segment Data
    if request.method == 'POST' and form.validate():

        # asign the variable value from request form value
        segment_type = request.form['segment_type']
        validity_date_start = request.form['validity_date_start']
        validity_date_finish = request.form['validity_date_finish']

        # Execute the query
        adminPriceSegmentModel.updatePriceSegment(segment_type, validity_date_start, validity_date_finish, price_segment_id)

        # Showing the notification
        flash('Price Segment ID  '+price_segment_id+' Updated', 'success')

        # Return the page of Price Segment Data Center
        return redirect(url_for('priceSegmentDataCenter'))

    return render_template('admin/priceSegmentEdit.html', form=form, price_segment_data=price_segment_data)
