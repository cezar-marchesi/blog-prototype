from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime(30),
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Post('{self.title}', '{self.date_posted}')"

    @classmethod
    def create_post(cls, title, content, author):
        post = cls(title=title,
                   content=content,
                   author=author)
        db.session.add(post)
        db.session.commit()
        return post

    @classmethod
    def get_all_posts(cls, page, author=None):
        if author:
            return Post.query.filter_by(author=author)\
                .order_by(Post.date_posted.desc())\
                .paginate(page=page, per_page=5)
        return Post.query.order_by(Post.date_posted.desc())\
            .paginate(page=page, per_page=5)

    @classmethod
    def get_post_by_id(cls, post_id):
        return Post.query.get_or_404(post_id)
    
    @classmethod
    def update_post(cls, post, form):
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

    @classmethod
    def delete_post(cls, post):
        db.session.delete(post)
        db.session.commit()
