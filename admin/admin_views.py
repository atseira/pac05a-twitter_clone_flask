from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for


class KlonxAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to the homepage
        return redirect('/')


class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            password = form.password.data
            model.set_password(password)
        return super(UserModelView, self).on_model_change(form, model, is_created)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to the homepage
        return redirect('/')


class TweetModelView(ModelView):
    def create_model(self, form):
        try:
            model = self.model()
            form.populate_obj(model)
            model.user_id = current_user.id
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            # Handle exceptions as you see fit
            return False
        return model
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to the homepage
        return redirect('/')

