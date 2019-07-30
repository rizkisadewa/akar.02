# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
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
    finish_date = StringField("Tanggal Pulang")
    total_pax = StringField("Total Peserta")
    destination = StringField()

@app.route('/')
def startIndex():
    # Fetch All Trip
    trip_data = adminTripModel.tripFetchData()

    # Fitting the Form
    form = PaketWisataCheckDestination(request.form)

    # check if the client press the submit button
    if request.method == 'POST' and form.validate():

        return redirect(url_for('clientServices'), destination)

    return render_template(
        'client/clientIndex.html',
        trip_data=trip_data,
        form=form
    )
