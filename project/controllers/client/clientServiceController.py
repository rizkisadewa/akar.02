# -*- coding: utf-8 -*-
from project import app
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask

# Import from Model
from project.models.adminTripModel import adminTripModel
from project.models.client.clientServicesModel import clientServicesModel

# an object from Model
adminTripModel = adminTripModel()
clientServiceModel = clientServicesModel()

# Service Route
@app.route('/paket-wisata/<string:destination>')
def clientServices(destination):

    # Fetch trip_id Refer to Destination
    trip_id = adminTripModel.tripIdFetchOneFromDestination(destination)

    # Fetch the Service Data refer to Trip ID
    service_data = clientServiceModel.clientServicesFetchData(trip_id['trip_id'])

    # Fetch all Destination Info
    destination_data = clientServiceModel.destinationFetchData()

    return render_template('client/clientServices.html',
    service_data=service_data,
    destination_data=destination_data,
    trip_id=trip_id,
    destination=destination)
