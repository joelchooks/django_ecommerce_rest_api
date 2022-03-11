from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, request
from django.contrib import messages
from time import sleep
from celery import shared_task


@shared_task
def send_user_email(subject, user_email, text_content, html_content):
    print('Initializing')
    msg = EmailMultiAlternatives(subject, text_content, 'admin@chuksbuy.herokuapp.com', [user_email], headers = {'Reply-To': 'joelchukks@gmail.com'})
    msg.attach_alternative(html_content, "text/html")
    print('Sending email...')
    msg.send()
    print('Email was successfully sent!')
