#!/usr/bin/env python
# coding=utf-8

import os
from flask import request
from werkzeug import secure_filename
from flask import render_template

from . import toolkit 
from .app import app

@app.route('/v1/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/yy/www/data/static/docker-compose/', filename))
            return toolkit.response({
                'result': 'success'
            })

    return render_template('upload.html') 
