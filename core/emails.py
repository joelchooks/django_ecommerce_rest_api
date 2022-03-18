from django import template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_user_email
from .tokens import account_activation_token



class CustomEmailSending():
    def __init__(self):
        pass

    def activate_user_email(self, user):
        subject = 'Activate Your ChuksBuy Account!'
        plaintext = template.loader.get_template('core/emails/activate_email_text.txt')
        htmltemp = template.loader.get_template('core/emails/activate_email_text.html')
        user_email = user.email
        c = {
            "email":user_email,
            'domain':'chuksbuy-prod.herokuapp.com',
            'site_name': 'ChuksBuy',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': account_activation_token.make_token(user),
            'protocol': 'http',
        }
        text_content = plaintext.render(c)
        html_content = htmltemp.render(c)
        send_user_email.delay(subject, user_email, text_content, html_content)

    
    def user_password_reset(self, user):
        subject = "Password Reset Requested"
        plaintext = template.loader.get_template('core/password/password_reset_email.txt')
        htmltemp = template.loader.get_template('core/password/password_reset_email.html')
        user_email = user.email
        c = {
            "email":user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'ChuksBuy',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
        }
        text_content = plaintext.render(c)
        html_content = htmltemp.render(c)
        send_user_email.delay(subject, user_email, text_content, html_content)