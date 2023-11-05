from flask_restful import Resource, Api, reqparse
from models.models import db, User, Tweet, Like
from flask import jsonify, request, current_app
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import uuid
from urllib.parse import urlparse, urlunparse
import os

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
    @jwt_required(optional=True)
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        paginated_tweets = Tweet.query.order_by(Tweet.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        tweets = []

        current_user_identity = get_jwt_identity()
        current_user = None
        if current_user_identity:
            current_username = current_user_identity['username']
            current_user = User.query.filter_by(username=current_username).first()

        for tweet in paginated_tweets.items:
            tweet_data = {
                'id': tweet.id,
                'content': tweet.content,
                'user_id': tweet.user_id,
                'username': tweet.user.username,
                'image_url': tweet.image_url,
                'likes': tweet.likes.count(),
                'liked': current_user.id in [like.user_id for like in tweet.likes] if current_user else False
            }
            tweets.append(tweet_data)

        # Include pagination info in the response
        return {
            'tweets': tweets,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_pages': paginated_tweets.pages,
                'total_items': paginated_tweets.total
            }
        }

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity={'username': user.username})
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class CurrentUserResource(Resource):
    @jwt_required()
    def get(self):
        username = get_jwt_identity()['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        user_data = {
            'id': user.id,
            'username': user.username,
            # ... any other user data fields you want to include
        }
        return {'user': user_data}, 200


class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        # You can perform any server-side cleanup here, such as blacklisting the token
        
        # The actual removal of the token should be done client-side
        return {'message': 'Logged out successfully'}, 200

class PostTweetResource(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.form['content']
            print("Received content:", content)

            # Fetch username from JWT identity and retrieve user ID
            current_username = get_jwt_identity()
            username = current_username['username']
            current_user = User.query.filter_by(username=username).first()
            
            if not current_user:
                return {'message': 'User not found'}, 404

            current_user_id = current_user.id

            # Extract the image file from the request if present
            image_file = request.files.get('image', None)
            image_url = None

            if image_file:
                print("Received image:")
                print("Filename:", image_file.filename)
                print("Content Type:", image_file.content_type)
                print("Size (in-memory):", len(image_file.read()), "bytes")

                # Rewind the file pointer to the start
                image_file.seek(0)

                # Get the Minio client from the Flask app
                minio_client = current_app.minio_client
                filename = secure_filename(image_file.filename)
                unique_filename = str(uuid.uuid4()) + '-' + filename
                bucket_name = current_app.config['MINIO_BUCKET']

                # Save the file temporarily and upload it
                temp_filepath = os.path.join("/tmp", unique_filename)
                image_file.save(temp_filepath)
                print("Size (on-disk):", os.path.getsize(temp_filepath), "bytes")

                minio_client.fput_object(
                    bucket_name, unique_filename,
                    temp_filepath,
                    content_type=image_file.content_type
                )

                # Remove the temporary file
                os.remove(temp_filepath)

                # Generate the direct image URL
                image_url = f"http://localhost:9000/{bucket_name}/{unique_filename}"
                            # Create a new tweet
                new_tweet = Tweet(content=content, user_id=current_user_id, image_url=image_url)
                db.session.add(new_tweet)
                db.session.commit()

                return {'id': new_tweet.id,
                        'content': new_tweet.content,
                        'user_id': new_tweet.user_id,
                        'image_url': new_tweet.image_url}

        except Exception as e:
                return {'message': str(e)}, 400

class LikeTweetResource(Resource):
    @jwt_required()
    def post(self, tweet_id):
        current_user_info = get_jwt_identity()
        current_username = current_user_info['username']

        # Fetch the user_id using the username
        current_user = User.query.filter_by(username=current_username).first()
        if not current_user:
            return {"message": "User not found"}, 404
        
        current_user_id = current_user.id
        
        tweet = Tweet.query.get_or_404(tweet_id)
        like = Like.query.filter_by(user_id=current_user_id, tweet_id=tweet_id).first()
        if not like:
            new_like = Like(user_id=current_user_id, tweet_id=tweet_id)
            db.session.add(new_like)
            db.session.commit()
            return {"message": "Tweet liked", "likes": tweet.likes.count()}, 200
        else:
            # Unlike the tweet
            db.session.delete(like)
            db.session.commit()
            return {"message": "Tweet unliked", "likes": tweet.likes.count()}, 200