from django.urls import path
# from django.views.generic import TemplateView
from . import views

app_name = 'core'
# URLConf
urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
]

# TemplateView.as_view(template_name='core/index.html', model=User.objects.all())