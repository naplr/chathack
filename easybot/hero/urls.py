from django.conf.urls import url, include
from django.contrib import admin
from . import views

uuid_regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^chat/$', views.chat),
    url(r'^bot-add/$', views.bot_add),
    url(r'^bot/(?P<bot_pk>{})/$'.format(uuid_regex), views.setup),
    url(r'^bot/(?P<bot_pk>{})/chat/$'.format(uuid_regex), views.chat),
    url(r'^bot/(?P<bot_pk>{})/add-intent/$'.format(uuid_regex), views.setup_add_intent),
    url(r'^bot/(?P<bot_pk>{})/edit-intent/(?P<pk>{})/'.format(uuid_regex, uuid_regex), views.setup_edit_intent),
    url(r'^api/accept-intent/',views.accept_intent),
    url(r'^api/reject-intent/', views.reject_intent),
    url(r'^chat-test/$', views.chat_test),
    url(r'^', views.bot_list),

]
