
import logging

from registry.user import forms
from registry.user import views
from registry.user import passwords
from flask_login import LoginManager
from passlib.context import CryptContext

logger = logging.getLogger(__name__)

class UserManager(object):

    def __init__(self, db_adapter, app=None,
                #view functions
                register_view_function=views.register,
                login_view_funcion=views.login, 
                logout_view_function=views.logout,
                modify_password_view_function=views.modify_password,
                unauthenticated_view_function=views.unauthenticated,
                profile_view_function = views.profile,
                #forms
                login_form = forms.LoginForm,
                register_form = forms.RegisterForm,
                #Misc
                login_manager = LoginManager()
                ):

        self.db_adapter = db_adapter
        self.register_view_function = register_view_function
        self.login_view_funcion = login_view_funcion
        self.logout_view_function = logout_view_function
        self.modify_password_view_function = modify_password_view_function
        self.profile_view_function = profile_view_function
        self.login_manager = login_manager
        self.unauthenticated_view_function = unauthenticated_view_function
        
        self.login_form = login_form
        self.register_form = register_form

        if app:
            self.init_app(app)

    def init_app(self, app):
        app.user_manager = self

        self.password_salt = app.config['SECRET_KEY']
        self.password_crypt_context = CryptContext(schemes='bcrypt') #TODO Add USER_PASSWORD_HASH to app.config
        self.setup_login_manager(app)
        self.add_url_routes(app)

    def setup_login_manager(self, app):

        @self.login_manager.user_loader
        def load_user_by_id(user_unicode_id):
            user_id = int(user_unicode_id)
            return self.get_user_by_id(user_id)

        self.login_manager.login_view = 'user.login'
        self.login_manager.init_app(app)

    def add_url_routes(self, app):
        app.add_url_rule('/v1/user/login', 'user.login', self.login_view_funcion, methods=['GET', 'POST'])
        app.add_url_rule('/v1/user/logout', 'user.logout', self.logout_view_function, methods=['GET', 'POST'])
        app.add_url_rule('/v1/user/register', 'user.register', self.register_view_function, methods=['GET', 'POST'])
        app.add_url_rule('/v1/user/modify-passsword', 'user.modify_password', self.modify_password_view_function, methods=['GET', 'POST'])
        app.add_url_rule('/v1/user/profile', 'user.profile', self.profile_view_function, methods=['GET'])

    def get_user_by_id(self, user_id):
        ObjectClass = self.db_adapter.UserClass 
        return self.db_adapter.get_object(ObjectClass, user_id)

    def find_user_by_username(self, username):
        ObjectClass = self.db_adapter.UserClass
        return self.db_adapter.find_first_object(ObjectClass, username=username)

    def find_user_by_email(self, email):
        ObjectClass = self.db_adapter.UserClass
        return self.db_adapter.find_first_object(ObjectClass, email=email)

    def hash_password(self, password):
        return passwords.hash_password(self, password)

    def get_password(self, user):
        pass

    def update_password(self, user, hashed_password):
        pass

    def verify_password(self, password, user):
        hashed_password =user.password
        return passwords.verify_password(self, password, hashed_password)

    def generate_token(self, user_id):
        pass

    def verfify_token(self, token, expiration_in_seconds):
        pass
