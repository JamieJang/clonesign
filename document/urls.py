from django.conf.urls import url

from . import views

app_name = "document"

urlpatterns =[ 
    url(r'^$',views.index.as_view(), name="docu-index"),
    url(r'^upload/$',views.UploadDocs.as_view(),name="upload-docs"),
    url(r'^self/$',views.selfDocs.as_view(),name="self-docs"),
    url(r'^by_partner/$', views.docsByPartner.as_view(), name="docs-by-partner"),
]
