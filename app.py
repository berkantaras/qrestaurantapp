from flask import Flask, redirect, url_for, request, session
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_security import Security, utils, SQLAlchemySessionUserDatastore
from flask_babelex import Babel
from database import db_session, init_db
from models import User, Role, Category
from views import UserAdmin, RoleAdmin,  CategoryAdmin
from api import api_bp



# Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(api_bp)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

# Create initial roles and users
@app.before_first_request
def create_user():
    init_db()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')
    db_session.commit()
    #user_datastore.create_user(email='user@example.com', password=utils.encrypt_password('user123'))
    #user_datastore.create_user(email='admin@example.com', password=utils.encrypt_password('admin123'))
    db_session.commit()
    user_datastore.add_role_to_user('user@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db_session.commit()



# Localize app
babel = Babel(app)

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'tr')



# Views
@app.route('/')
def home():
    return redirect(url_for('admin.index'))


	

# Add Flask-Admin views for Users and Roles
admin = Admin(app,
    name = 'QRestaurant',
    template_mode = 'bootstrap3',
    base_template='my_master.html'
)

admin.add_view(CategoryAdmin(Category, db_session, name='Kategoriler'))
admin.add_view(UserAdmin(User, db_session, name='Kullanıcılar'))
admin.add_view(RoleAdmin(Role, db_session, name='Kullanıcı Rolleri'))



# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


if __name__ == '__main__':
    app.run(debug=True)