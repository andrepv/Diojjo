from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth import views as auth_views

from authentication import views as diojo_auth_views
from account import views as account_views
from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^signup/', diojo_auth_views.signup, name='signup'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^login/$', auth_views.login, {
        'template_name': 'authentication/login.html'}, name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^ajax/validate_username/$', diojo_auth_views.validate_username,
        name='validate_username'),
    url(r'^profile/edit/$', account_views.edit, name='edit'),
    url(r'^profile/picture/$', account_views.picture, name='picture'),
    url(r'^profile/upload_picture/$', account_views.upload_picture,
        name='upload_picture'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
