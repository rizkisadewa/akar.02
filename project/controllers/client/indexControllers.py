# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField


# import from Model
from project.models.client.indexModel import indexModel
from project.models.adminServiceModel import adminServiceModel
from project.models.adminTripModel import adminTripModel

# an object from Index Model
indexModel = indexModel()
adminServiceModel = adminServiceModel()
adminTripModel = adminTripModel()

# Check Paket Wisata
class PaketWisataCheckDestination(Form):
    depart_date = StringField("Tanggal Berangkat")
    total_pax = StringField("Total Peserta")
    destination = StringField()

# Index
@app.route('/', methods=['GET','POST'])
def startIndex():
    # Fetch All Trip
    trip_data = adminTripModel.tripFetchData()

    # Fitting the Form
    form = PaketWisataCheckDestination(request.form)

    # check if the client press the submit button
    if request.method == 'POST' and form.validate():
        destination = form.destination.data
        total_pax = form.total_pax.data
        depart_date = form.depart_date.data

        return redirect(url_for('clientPackageTrip', destination=destination, total_pax=total_pax, depart_date=depart_date.format('DD-MM-YY')))

    return render_template(
        'client/clientIndex.html',
        trip_data=trip_data,
        form=form
    )
