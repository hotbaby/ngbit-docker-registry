
import time
from flask import request, current_user
from datetime import datetime
from registry import toolkit
from registry.app import app
from registry.core import compat
from registry.db import db

from .models import Comment
from registry.lib.index.db import Service


json = compat.json

@app.route('/v1/services/<service_name>/comments', methods=['GET', 'POST'])
def comment(service_name):

    #Handle GET request
    if request.method == 'GET':
        service = Service.query.filter_by(name=service_name)
        if service is None:
            return toolkit.response({
                'result': 'do not find service %s' % service_name
            })

        comments = Comment.query.filter_by(service_id=service.id)
        if comments is None:
            return toolkit.response([])
       
        results = []
        for comment in comments:
            timestamp = int(time.mktime(comment.create_time.utctimetuple()))
            obj = {
                'create_time': timestamp,
                'content': comment.comment,
                'user': comment.user.username
            }
            results.append(obj)
        return toolkit.response({ results })

    #Handle POST request
    data = request.data.decode('utf8')
    try:
        data = json.loads(data)
    except ValueError:
        return toolkit.api_error('Invalid data')

    service = Service.query.filter(name=service_name)
    if service == None:
        return toolkit.response({
            'result': 'do not find servcie %s' % service_name
        })

    try:
        comment = data['content']
        create_time = datetime.utcnow()
        db.session.add(Comment(comment=comment,
                               create_time=create_time,
                               ip=request.remote_addr,
                               user=current_user,
                               user_id=current_user.id,
                               servcie=service,
                               service_id=service.id))
        db.session.commit()

        timestamp = int(time.mktime(create_time.utctimetuple()))
        return toolkit.response({
            'create_time': timestamp,
            'content': data['content'],
            'user': current_user.username
        })

    except:
        return toolkit.api_error('Invalid data')

