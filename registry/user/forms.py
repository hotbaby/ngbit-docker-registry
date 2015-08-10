
from flask import current_app
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SubmitField

class LoginForm(Form):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def validate(self):
        user_manager = current_app.user_manager
        user = user_manager.find_user_by_username(self.username.data)
        result = user_manager.verify_password(self.password.data, user)
        if result == False:
            return False
        return True


class RegisterForm(Form):
    username = StringField('Username')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

    def validate(self):
        user_manager = current_app.user_manager
        user = user_manager.find_user_by_username(self.username.data)
        if user != None:
            return False
        user = user_manager.find_user_by_email(self.email.data)
        if user != None:
            return False
        return True


class ProfileForm(Form):
    pass

class ModifyPasswordForm(Form):
    pass
