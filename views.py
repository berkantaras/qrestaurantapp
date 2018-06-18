from flask import redirect, url_for, abort, request
from flask_security import current_user, utils
from flask_admin.contrib import sqla
from wtforms.fields import PasswordField

# Create customized model view class
class SecureModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# Customized User model for SQL-Admin
class UserAdmin(SecureModelView):

    # Humanize column labels
    column_labels = {
       'email': 'E-mail', 'username': 'Kullanıcı Adı', 'last_login_at': 'Önceki Giriş Tarihi', 'current_login_at': 'Son Giriş Tarihi',
        'last_login_ip': 'Önceki IP', 'current_login_ip': 'Son IP', 'login_count': 'Giriş sayısı', 'active': 'Etkin',
        'confirmed_at': 'Doğrulanma Tarihi', 'roles': 'Roller', 'roles.name': 'Rol'
    }

    # Don't display the password on the list of Users
    column_exclude_list = ['password']

    # Don't include the standard password field when creating or editing a User (but see below)
    # as well as date time and IP fields
    form_excluded_columns = [
        'password', 'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip', 'login_count', 'confirmed_at'
    ]

    # Filter by role and status
    column_filters = ['active', 'roles.name']

    # Search by username and email
    column_searchable_list = ['username', 'email']

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    # On the form for creating or editing a User, don't display a field corresponding to the model's password field.
    # There are two reasons for this. First, we want to encrypt the password before storing in the database. Second,
    # we want to use a password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('Yeni Parola')
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited User -- before the changes
    # are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank
        if len(model.password2):

            # then encrypt the new password prior to storing it in the database. If the password field is blank,
            # the existing password in the database will be retained.
            model.password = utils.encrypt_password(model.password2)



# Customized Role model for SQL-Admin
class RoleAdmin(SecureModelView):

    # Humanize column labels
    column_labels = {'name': 'Ad', 'description': 'Açıklama'}

    # don't open new page for simple forms
    create_modal = True
    edit_modal = True



class CategoryAdmin(SecureModelView):

    # Exclude unnecessary fields from form
    form_excluded_columns = ['created_at', 'updated_at']

    # Humanize column labels
    column_labels = dict(name='Ad', created_at='Eklendi', updated_at='Düzenlendi')

    # don't open new page for simple forms
    create_modal = True
    edit_modal = True
