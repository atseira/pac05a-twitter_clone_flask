from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


# Initialize database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False


    # Initialize database with app
    db.init_app(app)

    from models.models import User, Tweet  # Import models
    from admin.admin_views import UserModelView, TweetModelView

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return {'message': 'Please log in to access this page.'}, 401


    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return current_user.is_authenticated

    # Initialize Flask-Admin
    admin = Admin(app, index_view=MyAdminIndexView())
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(TweetModelView(Tweet, db.session))

    # Login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect('/admin')
        return render_template('login.html')

    # Logout route
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/login')

    from api.resources import Api, TweetsResource, LoginResource, LogoutResource, PostTweetResource

    api = Api(app)

    # Add API resources
    # api.add_resource(UserResource, '/api/users/<int:user_id>')
    # api.add_resource(TweetResource, '/api/tweets/<int:tweet_id>')
    api.add_resource(TweetsResource, '/api/tweets')  # Add this line for the new endpoint
    api.add_resource(LoginResource, '/api/login')  # Add this line for the new login endpoint
    api.add_resource(PostTweetResource, '/api/post-tweet')  # Add this line for the new endpoint
    api.add_resource(LogoutResource, '/api/logout')

    from flask_cors import CORS

    CORS(app, supports_credentials=True)  # This will enable CORS for all routes

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
