from flask_login import current_user
from wtforms.validators import ValidationError
from app.users.models import User


class UsernameExists:
    def __call__(self, form, field) -> None:
        if not current_user.is_authenticated or field.data != current_user.username:
            username = User.query.filter_by(username=field.data).first()
            if username:
                raise ValidationError("Username already exists")


class EmailExists:
    def __call__(self, form, field) -> None:
        if not current_user.is_authenticated or field.data != current_user.email:
            email = User.query.filter_by(email=field.data).first()
            if email:
                raise ValidationError("Email already exists")

class EmailDoesNotExist:
    def __call__(self, form, field) -> None:
        if not current_user.is_authenticated or field.data != current_user.email:
            email = User.query.filter_by(email=field.data).first()
            if email is None:
                raise ValidationError("Email does not exist. Register first")