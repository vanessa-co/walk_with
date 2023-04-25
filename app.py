import secrets
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User, Walk, Review, Follow
from config import app, api

# JWT configuration
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)  # Generate a 256-bit (32-byte) secret key
jwt = JWTManager(app)

class Home(Resource):
    def get(self):
        return 'HomePage'
       
api.add_resource(Home, '/')

def user_exists(username, email):
    return User.query.filter((User.username == username) | (User.email == email)).first() is not None

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        if user_exists(data['username'], data['email']):
            return {"message": "User already exists"}, 400

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']  # You should hash the password before saving it
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and user.password == data['password']:  # You should verify the hashed password
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}, 200
        else:
            return {"message": "Invalid credentials"}, 401


class UserWalks(Resource):
    @jwt_required()
    def get(self, user_id):
        walks = Walk.query.filter_by(user_id=user_id).all()
        return jsonify([walk.serialize() for walk in walks])

    @jwt_required()
    def post(self, user_id):
        data = request.get_json()
        new_walk = Walk(
            location=data['location'],
            distance=data['distance'],
            photo=data['photo'],
            user_id=user_id
        )
        db.session.add(new_walk)
        db.session.commit()
        return {"message": "Walk created successfully"}, 201

class WalkSearch(Resource):
    def get(self):
        location = request.args.get('location')
        walks = Walk.query.filter(Walk.location.ilike(f"%{location}%")).all()
        return jsonify([walk.serialize() for walk in walks])


class WalkReviews(Resource):
    @jwt_required()
    def get(self, walk_id):
        walk = Walk.query.get_or_404(walk_id)
        reviews = walk.reviews
        return jsonify([review.to_dict() for review in reviews])

    @jwt_required()
    def post(self, walk_id):
        data = request.get_json()
        user_id = get_jwt_identity()
        new_review = Review(
            text=data['text'],
            user_id=user_id,
            walk_id=walk_id
        )
        db.session.add(new_review)
        db.session.commit()
        return {"message": "Review created successfully"}, 201

class UserFollow(Resource):
    @jwt_required()
    def post(self, user_id):
        follower_id = get_jwt_identity()
        if user_id == follower_id:
            return {"message": "You cannot follow yourself"}, 400

        follow = Follow.query.filter_by(follower_id=follower_id, followed_id=user_id).first()
        if follow:
            return {"message": "Already following"}, 400

        new_follow = Follow(
            follower_id=follower_id,
            followed_id=user_id
        )
        db.session.add(new_follow)
        db.session.commit()
        return {"message": "User followed successfully"}, 201

    @jwt_required()
    def delete(self, user_id):
        follower_id = get_jwt_identity()
        follow = Follow.query.filter_by(follower_id=follower_id, followed_id=user_id).first()
        if not follow:
            return {"message": "Not following"}, 400

        db.session.delete(follow)
        db.session.commit()
        return {"message": "User unfollowed successfully"}, 200

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserWalks, '/user/<int:user_id>/walks')
api.add_resource(WalkSearch, '/search')
api.add_resource(WalkReviews, '/walk/<int:walk_id>/reviews')
api.add_resource(UserFollow, '/user/<int:user_id>/follow')




if __name__ == '__main__':
    app.run(port=5555, debug=True)    