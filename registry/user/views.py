
import json
import logging

from registry import toolkit
from registry.user.models import User
from registry.user.decorators import login_required
from flask import current_app, flash, request, url_for, render_template, redirect
from flask_login import current_user, login_user, logout_user

logger = logging.getLogger(__name__)

def register():
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter
    register_form = user_manager.register_form(request.form)

    if request.method == 'GET':
        return render_template('register.html',
                               form=register_form,
                               user_manager=user_manager)

    # POST request
    content_type = request.headers.get('Content-Type')
    if content_type.lower() ==  'application/json':
        data = json.loads(request.data.decode('utf8'))
        username = data.get('username', None)
        password = data.get('password', None)
        email = data.get('email', None)
    
        error_message = None
        if username is None:
            error_message = 'username is None'
        elif password is None:
            error_message = 'password is None'
        elif email is None:
            error_message = 'email is None'
        else:
            pass
        if error_message != None:
            return toolkit.response({
                'result': error_message
            })

        user_fileds = {}

        #Verify whether usrname has registed or not.
        object = db_adapter.find_first_object(User, username=username)
        if object != None:
            return toolkit.response({
                'result': 'user has registed'
            })
        user_fileds['username'] = username
            
        #Verify whether email has registed or not.
        object = db_adapter.find_first_object(User, email=email)
        if object != None:
            return toolkit.response({
                'result': 'email has registed'
            })
        user_fileds['email'] = email

        #Hash password
        user_fileds['password'] = user_manager.hash_password(password)

        db_adapter.add_object(User, **user_fileds)
        db_adapter.commit()
        return toolkit.response({
            'result': 'success'
        })
    else:
        if register_form.validate() == False:
            return toolkit.response({
                'result': 'failure'
            })

        user_fileds = {}
        user_fileds['username'] = register_form.username.data
        user_fileds['password'] = user_manager.hash_password(register_form.password.data)
        user_fileds['email'] = register_form.email.data
        db_adapter.add_object(User, **user_fileds)
        db_adapter.commit()
        return redirect('/v1/user/login')


def login():
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    login_form = user_manager.login_form(request.form)
    if request.method == 'GET':
        return render_template('login.html', 
                               form=login_form,
                               user_manager=user_manager)

    # POST reqest
    next = request.args.get('next', None)
    content_type = request.headers.get('Content-Type', None)
    if content_type.lower() == 'application/json':
        data = json.loads(request.data.decode('utf8'))
        username = data.get('username', None)
        password = data.get('password', None)

        error_message = None
        if username is None:
            error_message = 'username can not be empty'
        elif password is None:
            error_message = 'password can bot be empty'
        else:
            pass
        if error_message != None:
            return toolkit.response({
                'result': error_message
            })

        user = db_adapter.find_first_object(User, username=username)
        if user is None:
            return toolkit.response({
                'result': 'username is not exited'
            })
    
        #Verify password
        result = user_manager.verify_password(password, user)
        if result == False:
            return toolkit.response({
                'result': 'password  error'
            })

        result = login_user(user, remember=True)
        if result == True:
            return toolkit.response({
                'result': 'success'
            })
        else:
            return toolkit.response({
                'result': 'failure'
            })

    else:
        if login_form.validate() == False:
            return toolkit.response({
                'result': 'failure'
            })
    
        user = user_manager.find_user_by_username(login_form.username.data)
        remember = login_form.remember_me.data
        result = login_user(user, remember)
        if result == False:
            return toolkit.response({
                'result': 'failure'
            })

        if next != None:
            return redirect(next)
        return redirect('/')
 
@login_required
def logout():
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    # POST request
    content_type = request.headers.get('Content-Type')
    if content_type.lower() == 'application/json':
        #data = json.loads(request.data.decode('utf8'))
        logout_user()

        return toolkit.response({
            'result': 'success'
        })
    else:
        next = request.args.get('next', None)
        logout_user()
        
        if next != None:
            return redirect(next)
        return redirect('/')

@login_required
def modify_password():
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    if request.method == 'POST':
        pass

    return render_template('base.html')

@login_required
def profile():
    user_manager = current_app.user_manager
    db_adapter = user_manager.db_adapter

    content_type = request.headers.get('Content-Type')
    if content_type.lower() == 'application/json':
        return toolkit.response({
            'result': 'success'
        })
    else:
        return render_template('profile.html', user_manager=user_manager)

def unauthenticated():
    return toolkit.response({
        'result': 'unauthenticated'
    })
