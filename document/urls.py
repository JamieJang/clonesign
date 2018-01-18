from django.conf.urls import url

from . import views

app_name = "document"

urlpatterns =[ 
    url(r'^$',views.index.as_view(), name="docu-index"),
]