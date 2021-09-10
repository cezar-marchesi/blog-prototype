import secrets
import os
from dotenv import load_dotenv
from PIL import Image
from flask import url_for, current_app
from app import mail
from flask_mail import Message


load_dotenv()


def save_image(form_image, current_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_pics', image_fn)

    output_size = (125, 125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    if current_image != 'default.jpg':
        image_path = os.path.join(
            current_app.root_path, 'static/profile_pics', current_image)
        os.remove(image_path)

    return image_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset',
                  sender=os.environ.get('EMAIL_USER'),
                  recipients=[user.email])

    msg.body = f'''To reset your passwor, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request simply ignore this email.
'''                  
    mail.send(msg)
