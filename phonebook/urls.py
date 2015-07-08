
from django.conf.urls import patterns, include, url

from .views import Contacts
urlpatterns = [
    url(r'^contacts(\.(?P<_format>[a-zA-Z]+))?/?$', Contacts.as_view()),
    url(r'^contacts/(?P<contact_id>[0-9]+)(\.(?P<_format>[a-zA-Z]+))?/?$',
        Contacts.as_view()),
]
