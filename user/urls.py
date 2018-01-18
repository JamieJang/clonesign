from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

app_name = "user"

urlpatterns = [
    url(r'^$',RedirectView.as_view(url="/signup")),
    url(r'^signup',views.signup.as_view(),name="signup"),
]