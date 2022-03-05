from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customers


def say_hello(request):
    notify_customers.delay('Hello')

    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Emeka'}
    #     )    
    #     message.attach_file('playground/static/images/car.jpeg')
    #     message.send(['admin@chuksbuy.com', 'customer@gmail.com'])
    # except BadHeaderError:
    #     pass
    return render(request, 'hello.html', {'name': 'Emeka'})
