from flask_restful import Resource, Api, reqparse
from models.models import db, User, Tweet
from flask import jsonify, request
from werkzeug.security import check_password_hash
from flask_login import login_required, current_user, login_user, logout_user


parser = reqparse.RequestParser()
parser.add_argument('page', type=int, required=False, default=1, help='Page number')
parser.add_argument('per_page', type=int, required=False, default=10, help='Items per page')

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify({'username': user.username})

class TweetResource(Resource):
    def get(self, tweet_id):
        tweet = Tweet.query.get_or_404(tweet_id)
        return jsonify({'content': tweet.content, 'user_id': tweet.user_id})



class TweetsResource(Resource):
    def get(self):
        page = int(request.args.get('page', 1))  # Use Flask's native request.args
        per_page = int(request.args.get('per_page', 10))
        
        paginated_tweets = Tweet.query.paginate(page=page, per_page=per_page, error_out=False)
        tweets = []
        for tweet in paginated_tweets.items:
            tweet_data = {
                'id': tweet.id,
                'content': tweet.content,
                'user_id': tweet.user_id,
                'username': tweet.user.username
            }
            tweets.append(tweet_data)
        
        return {'tweets': tweets}

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            print("Success login")
            return {'status': 'success', 'message': 'Logged in successfully', 'user': {'username': user.username}}, 200
        else:
            print("Failed login")
            return {'status': 'fail', 'message': 'Invalid credentials'}, 401

class LogoutResource(Resource):
    def post(self):
        logout_user()
        return {'message': 'Logged out successfully'}, 200

class PostTweetResource(Resource):
    @login_required
    def post(self):
        try:
            data = request.json
            content = data['content']
            new_tweet = Tweet(content=content, user_id=current_user.id)
            db.session.add(new_tweet)
            db.session.commit()
            return {'id': new_tweet.id, 'content': new_tweet.content, 'user_id': new_tweet.user_id}
        except Exception as e:
            return {'message': str(e)}, 400
