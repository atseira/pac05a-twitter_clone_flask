from flask_restful import Resource, Api, reqparse
from models.models import User, Tweet
from flask import jsonify

parser = reqparse.RequestParser()
parser.add_argument('page', type=int, required=False, default=1, help='Page number')
parser.add_argument('per_page', type=int, required=False, default=10, help='Items per page')

class TweetsResource(Resource):
    def get(self):
        args = parser.parse_args()
        page = args['page']
        per_page = args['per_page']
        
        paginated_tweets = Tweet.query.paginate(page, per_page, error_out=False)
        tweets = []
        for tweet in paginated_tweets.items:
            tweet_data = {
                'id': tweet.id,
                'content': tweet.content,
                'user_id': tweet.user_id,
                'username': tweet.user.username
            }
            tweets.append(tweet_data)
        
        return jsonify({'tweets': tweets})
