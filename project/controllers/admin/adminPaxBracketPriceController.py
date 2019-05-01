# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, FloatField, TimeField, IntegerField, DecimalField
from functools import wraps

# Import from Model
from project.models.adminPackageExcursionModel import adminPackageExcursionModel
from project.models.adminPaxBracketPriceModel import adminPaxBracketPriceModel
from project.models.adminPriceSegmentModel import adminPriceSegmentModel

# an object from Admin Model
adminPackageExcrusionModel = adminPackageExcursionModel()
adminPaxBracketPriceModel = adminPaxBracketPriceModel()
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

# Add Pax Bracket Price Form Class
class AddPaxBracketPrice(Form):
    min_pax = IntegerField(u'Minimum Pax')
    max_pax = IntegerField(u'Maximum Pax')
    price_per_person = FloatField(u'Price Per Person')
    segment_type = StringField()

# Add Pax Bracket Price
@app.route('/admin/package-excursion/pax-bracket-price/<string:package_excursion_id>', methods=['GET', 'POST'])
@is_logged_in
def paxBracketPriceDataCenter(package_excursion_id):

    # Fit the Pax Bracket Price Form Class
    form = AddPaxBracketPrice(request.form)

    # Fetch One Package Excrusion Data
    package_excursion_data = adminPackageExcrusionModel.packageExcursionDataFetchOne(package_excursion_id)

    # Fetch Price Segment Data
    price_segment_data = adminPriceSegmentModel.priceSegmentFetchData()

    # Fetch All Pax Bracket Price
    pax_bracket_price_data = adminPaxBracketPriceModel.paxBracketPriceFetchData()

    # Add the data
    if request.method == 'POST' and form.validate():
        min_pax = form.min_pax.data
        max_pax = form.max_pax.data
        price_per_person = form.price_per_person.data
        segment_type = form.segment_type.data
        # Fetch Price Segment ID refer to the segment_type input in the form
        price_segment_id = adminPaxBracketPriceModel.priceSegmentIdFetchOne(segment_type)

        # Execute query : add the data into the database
        adminPaxBracketPriceModel.addPaxBracketPrice(min_pax, max_pax, price_per_person, price_segment_id["price_segment_id"])

        # showing the notification to the dashboard
        flash('Pax Bracket Price has been updated', 'success')

        # Redirect to the same url
        return redirect('/admin/package-excursion/pax-bracket-price/'+package_excursion_id)

    return render_template('admin/paxBracketPrice.html', package_excursion_data=package_excursion_data, form=form, price_segment_data=price_segment_data, pax_bracket_price_data=pax_bracket_price_data)

# Delete Pax Bracket Price
@app.route('/admin/package-excursion/pax-bracket-price/delete/<string:pax_bracket_price_id>?<string:package_excursion_id>', methods=['GET', 'POST'])
@is_logged_in
def deletePaxBracketPrice(pax_bracket_price_id, package_excursion_id):

    # execute query in model
    adminPaxBracketPriceModel.deletePaxBracketPrice(pax_bracket_price_id)

    # show flash message in dashboard
    flash('Pax Bracket ID '+pax_bracket_price_id+' has been deleted', 'danger')

    # Redirect to the same url
    return redirect('/admin/package-excursion/pax-bracket-price/'+package_excursion_id)
