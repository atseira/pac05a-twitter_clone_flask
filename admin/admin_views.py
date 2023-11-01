from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            password = form.password.data
            model.set_password(password)
        return super(UserModelView, self).on_model_change(form, model, is_created)

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
