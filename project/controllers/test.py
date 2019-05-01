# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.route('/test')
def startTest():
    return render_template('printer/test.html')
