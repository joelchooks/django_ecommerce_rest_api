from asyncio.log import logger
from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.http import response
from django.shortcuts import render
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from templated_mail.mail import BaseEmailMessage
from rest_framework.views import APIView
from .tasks import notify_customers
import requests
import logging


logging.getLogger(__name__) 


class HelloView(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recieved the response')
            data = response.json()
        except request.ConnectionError:
            logger.critical('Httpbin is offline')
        return render(request, 'hello.html', {'name': data})


# def say_hello(request):
#     key = 'httpbin_result'

#     if cache.get(key) is None:
#         response = requests.get('https://httpbin.org/delay/2')
#         data = response.json()
#         cache.set(key, data)
    
    # notify_customers.delay('Hello')

    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Emeka'}
    #     )    
    #     message.attach_file('playground/static/images/car.jpeg')
    #     message.send(['admin@chuksbuy.com', 'customer@gmail.com'])
    # except BadHeaderError:
    #     pass
    # return render(request, 'hello.html', {'name': data})
