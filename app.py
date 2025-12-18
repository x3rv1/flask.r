from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    posts = db.relationship('Post', back_populates='user', cascade='all, delete-orphan')

    # Serialization rules
    serialize_rules = ('-posts.user',)

# Association table for Many-to-Many
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    # Serialization rules
    # Prevent recursion: Stop seeing 'posts' inside 'tags', and 'user' inside 'posts' (already done)
    serialize_rules = ('-user.posts', '-tags.posts')

class Tag(db.Model, SerializerMixin):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')

    # Serialization rules
    serialize_rules = ('-posts.tags',)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    # to_dict() is provided by SerializerMixin
    return make_response(jsonify([user.to_dict() for user in users]), 200)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        new_user = User(name=data['name'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
