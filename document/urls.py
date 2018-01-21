from django.conf.urls import url

from . import views

app_name = "document"

urlpatterns =[ 
    url(r'^$',views.index.as_view(), name="docu-index"),
    url(r'^upload/$',views.UploadDocs.as_view(),name="upload-docs"),
    url(r'^self/$',views.selfDocs.as_view(),name="self-docs"),
    url(r'^by_partner/$', views.docsByPartner.as_view(), name="docs-by-partner"),
    url(r'^filter/status/(?P<status>[\w\W]+)/$',views.docsByStatus.as_view(),name="filter_by_status"),
    url(r'^search/(?P<keyword>[ㄱ-힣\w]+)/$',
        views.docsByKeyword.as_view(), name="search_keyword"),
    url(r'^profile/$',views.Profile.as_view(),name="profile"),
    url(r'^userinfo/$',views.ChangeUsername.as_view(), name="userinfo"),
    url(r'^password/$',views.ChangePassword.as_view(),name="change_password"),
    url(r'^docs/(?P<pk>\d+)/del/$',views.DeleteDocs.as_view(),name="delete_docs"),
    url(r'^own_template/$',views.OwnTemplate.as_view(), name="own_template"),
    url(r'^own_template/create/$',views.CreateOwnTemplate.as_view(), name="create_own_template"),
    url(r'^own_template/(?P<pk>\d+)/$',views.DetailOwnTemplate.as_view(), name="detail_own_template"),
    url(r'^own_template/(?P<pk>\d+)/del/$',views.DeleteTemplate.as_view(), name="delete_template"),
]
