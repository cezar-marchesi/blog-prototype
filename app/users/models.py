from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app import db, bcrypt, login_manager
from flask import current_app
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username=username,
                   email=email,
                   password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def update_user(cls, user, form):
        from app.utils.helpers import save_image
        if form.image_file.data:
            user.image_file = save_image(
                form.image_file.data, user.image_file)
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
    
    @classmethod
    def get_user(cls, **kwargs):
        if 'username' in kwargs.keys():
            return User.query.filter_by(username=kwargs['username']).first_or_404()
        elif 'email' in kwargs.keys():
            return User.query.filter_by(email=kwargs['email']).first()
    
    @classmethod
    def reset_password(cls, user, form):
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod 
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
