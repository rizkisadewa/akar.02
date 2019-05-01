# -*- coding: utf-8 -*-
from project import app
from flask import Flask
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask

# Import from Model
from project.models.client.clientServicesModel import clientServicesModel
from project.models.client.clientServiceDetailModel import clientServiceDetailModel

# an object from Model
clientServiceModel = clientServicesModel()
clientServiceDetailModel = clientServiceDetailModel()


# Service Detail Route
@app.route('/paket-wisata/<string:destination>/<string:name_of_service>/<string:service_id>')
def clientServiceDetail(destination, name_of_service, service_id):

    # Fetch all Destination Info
    destination_data = clientServiceModel.destinationFetchData()
    destination_srv_dtl_data = clientServiceDetailModel.destinationSrvDtlFetchOneData(service_id)
    service_image_data = clientServiceDetailModel.serviceImageDataFetchData(service_id)
    program_detail_data = clientServiceDetailModel.programDetailFetchOne(service_id)

    return render_template('client/clientServiceDetail.html',
    destination_data=destination_data,
    destination_srv_dtl_data=destination_srv_dtl_data,
    service_image_data=service_image_data,
    program_detail_data=program_detail_data,
    destination=destination)
