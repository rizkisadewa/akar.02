# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request

# import from Model
from project.models.client.indexModel import indexModel

# an object from Index Model
indexModel = indexModel()

@app.route('/')
def startIndex():

    # Fetch Data of Trip Data
    trip_data = indexModel.tripFetchData()


    return render_template('client/clientIndex.html', trip_data=trip_data)
