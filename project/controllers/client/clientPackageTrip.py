# -*- coding: utf-8 -*-
from project import app
from flask import render_template, flash, redirect, url_for, session, request, logging #stuff from Flask
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, DateField, TimeField


# Showing Package Trip Option
@app.route('/paket-wisata/<string:destination>/<string:total_pax>/<string:depart_date>')
def clientPackageTrip(destination, total_pax, depart_date):

    return render_template('client/clientPackageTrip.html')
