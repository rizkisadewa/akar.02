# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

#import from Model
from project.models.adminModels import adminModel

# an object from Admin Models
adminModel = adminModel()


#import from Admin Validation
from project.controllers.admin.adminValidationsController import adminValidation
adminValidation = adminValidation()

# Register Class
class RegisterForm(Form):
    admin_name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')

# Register for Admin
@app.route('/admin/register', methods=['GET', 'POST'])
def adminRegister():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        admin_name = form.admin_name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # implemntation of function Admin Register from Admin Model
        adminModel.registerAdmin(admin_name, email, username, password)

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('adminLogin'))

    return render_template('admin/adminRegister.html', form=form)

# Login Admin
@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    if request.method == 'POST':
        #Get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        url = url_for('adminDashboard')

        if adminValidation.adminLogin(username, password_candidate) == True:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('adminDashboard'))

    return render_template('admin/adminLogin.html')

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

# Logout
@app.route('/admin/logout')
@is_logged_in
def adminLogout():
    return adminValidation.adminLogout()

# go to Admin Dashboard
@app.route('/admin/dashboard')
@is_logged_in
def adminDashboard():
    # Fetch Data

    return render_template('/admin/adminIndex.html')

# Add Vendor Data Form Class
class AddVendorData(Form):
    vendor_type = StringField('Type Of Vendor', [validators.Length(min=1, max=100)])

# Add Vendor Data Setting
@app.route('/admin/vendordata', methods=['GET', 'POST'])
@is_logged_in
def vendorData():

    #Fetch Data of Vendor Data
    vendor_datas = adminModel.vendorFetchData()

    #Add The Vendor Data
    form = AddVendorData(request.form)
    if request.method == 'POST' and form.validate():
        vendor_type = form.vendor_type.data

        adminModel.addVendorData(vendor_type)

        flash('Vendor Added', 'success')

        return redirect(url_for('vendorData'))
    return render_template('admin/vendorData.html', form=form, vendor_datas=vendor_datas)

# Edit Vendor Data
# /admin/vendor-data/edit/{{vendor_data.vendor_id}}
@app.route('/admin/vendordata/edit/<string:vendor_id>', methods=['GET', 'POST'])
@is_logged_in
def vendorDataEdit(vendor_id):
    #Fetch One Vendor Data
    vendor_data = adminModel.vendorDataFetchOne(vendor_id)

    #Add The Vendor Data
    form = AddVendorData(request.form)

    # Populate article from fields
    form.vendor_type.data = vendor_data['vendor_type']

    # Update The Vendor Data
    if request.method == 'POST' and form.validate():
        vendor_type = request.form['vendor_type']

        adminModel.editVendorDAta(vendor_type, vendor_id)

        flash('Vendor ID '+vendor_id+' Updated', 'success')

        return redirect(url_for('vendorData'))
    return render_template('admin/vendorDataEdit.html', form=form)

# Delete Vendor Data
@app.route('/admin/vendordata/delete/<string:vendor_id>', methods=['POST'])
@is_logged_in
def deleteVendorData(vendor_id):

    adminModel.deleteVendorData(vendor_id)

    flash('Vendor ID '+vendor_id+' Deleted', 'danger')

    return redirect(url_for('vendorData'))
