from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

from . import views

app_name = "user"

urlpatterns = [
    url(r'^$',RedirectView.as_view(url="/signup")),
    url(r'^signup/$',views.signup.as_view(),name="signup"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^login/$',auth_views.login, {"template_name":"user/login.html"}, name="login"),
    url(r'^logout/$',auth_views.logout, {'next_page':'/'}),
]
