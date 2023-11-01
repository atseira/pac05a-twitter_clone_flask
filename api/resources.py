from flask_restful import Resource, Api, reqparse
from models.models import User, Tweet
from flask import jsonify, request

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
