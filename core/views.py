from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.views.generic import ListView
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.db import transaction
from .models import User
from .forms import NewUserForm
from .emails import CustomEmailSending
from .tokens import account_activation_token


class IndexTemplateView(ListView):
    queryset = User.objects.all()
    template_name = 'core/index.html'
    context_name = {'user': queryset}

def register_request(request):
    with transaction.atomic():
        if request.method == 'POST':
            form = NewUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_instance = CustomEmailSending()
                email_instance.activate_user_email(user)

                # subject = 'Activate Your ChuksBuy Account!'
                # plaintext = template.loader.get_template('core/emails/activate_email_text.txt')
                # htmltemp = template.loader.get_template('core/emails/activate_email_text.html')
                # user_email = user.email
                # c = {
                #     "email":form.cleaned_data.get('email'),
                #     'domain':'chuksbuy-prod.herokuapp.com',
                #     'site_name': 'ChuksBuy',
                #     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                #     "user": user,
                #     'token': account_activation_token.make_token(user),
                #     'protocol': 'http',
                # }
                # text_content = plaintext.render(c)
                # html_content = htmltemp.render(c)
                # send_user_email.delay(subject, user_email, text_content, html_content)
                # msg = EmailMultiAlternatives(subject, text_content, 'admin@chuksbuy.herokuapp.com', [user_email], headers = {'Reply-To': 'joelchukks@gmail.com'})
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                return redirect('core:confirm_email')            
            messages.error(
                request,
                'Unsuccessful Registration. Either the user already exists or the information is invalid!'
            )
    form = NewUserForm()
    return render(request, 'core/register.html', context={'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(
            request,
            'Thank you for confirming your email address. Registration Successful!'
        )
        return redirect('core:index')
    else:
        return HttpResponse('Activation link is invalid!')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active: 
                    email_instance = CustomEmailSending()
                    email_instance.activate_user_email(user)
                    messages.info(request,"A new verification mail has been sent to you email address.Please activate your account and try logging in again.")
                else:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("core:index")
            else:
                messages.error(request,"user with username and password does not exist.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="core/login.html", context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("core:index")



def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email_instance = CustomEmailSending()
                    email_instance.user_password_reset(user)
                    # subject = "Password Reset Requested"
                    # plaintext = template.loader.get_template('core/password/password_reset_email.txt')
                    # htmltemp = template.loader.get_template('core/password/password_reset_email.html')
                    # user_email = user.email
                    # c = {
                    #     "email":user.email,
                    #     'domain':'127.0.0.1:8000',
                    #     'site_name': 'ChuksBuy',
                    #     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    #     "user": user,
                    #     'token': default_token_generator.make_token(user),
                    #     'protocol': 'http',
                    # }
                    # text_content = plaintext.render(c)
                    # html_content = htmltemp.render(c)
                    # send_user_email.delay(subject, user_email, text_content, html_content)
                        # msg = EmailMultiAlternatives(subject, text_content, 'admin@chuksbuy.herokuapp.com', [user.email], headers = {'Reply-To': 'joelchukks@gmail.com'})
                        # msg.attach_alternative(html_content, "text/html")
                        # msg.send()
                    return redirect ("password_reset_requested")
    password_reset_form = PasswordResetForm()
    return render(request, template_name="core/password/password_reset.html", context={"password_reset_form":password_reset_form})