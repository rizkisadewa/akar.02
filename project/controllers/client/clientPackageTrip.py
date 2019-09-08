# -*- coding: utf-8 -*-
from project import app
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField

# import from Model
from project.models.client.clientPackageTripModel import clientPackageTripModel

# an object from Admin Models
clientPackageTripModel = clientPackageTripModel()

# Showing Package Trip Option
@app.route('/paket-wisata/<string:destination>/<string:total_pax>/<string:depart_date>')
def clientPackageTrip(destination, total_pax, depart_date):

    # Obtaining the trip_id from destination
    trip_id = clientPackageTripModel.tripIdFetchOne(destination)

    # Obtaining the service_id from trip_id
    service_id = clientPackageTripModel.serviceIdFetchOne(trip_id["trip_id"])

    # Fetch the All Package Service
    package_trip_options_data = clientPackageTripModel.packageTripOptionsFetchData(trip_id["trip_id"], service_id["service_id"], total_pax, total_pax)

    return render_template(
        'client/clientPackageTrip.html',
        package_trip_options_data=package_trip_options_data,
        total_pax = total_pax
    )
