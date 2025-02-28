# -*- coding: utf-8 -*-

from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from . import views

admin.autodiscover()

staff_required = user_passes_test(lambda u: u.is_staff)

superuser_required = user_passes_test(lambda u: u.is_superuser)

run_permission = user_passes_test(lambda u: u.has_perm('bots.change_mutex'))

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # login required
    path('home/', login_required(views.home), name='home'),
    path('incoming/', login_required(views.incoming), name='incoming'),
    path('detail/', login_required(views.detail), name='detail'),
    path('process/', login_required(views.process), name='process'),
    path('outgoing/', login_required(views.outgoing), name='outgoing'),
    path('document/', login_required(views.document), name='document'),
    path('reports/', login_required(views.reports), name='reports'),
    path('confirm/', login_required(views.confirm), name='confirm'),
    path('filer/', login_required(views.filer), name='filer'),
    path('srcfiler/', login_required(views.srcfiler), name='srcfiler'),
    path('logfiler/', login_required(views.logfiler), name='logfiler'),
    # only staff - admin site
    path('admin/', admin.site.urls),
    path('runengine/', run_permission(views.runengine), name='runengine'),
    # only superuser
    path('delete/', superuser_required(views.delete), name='delete'),
    path('plugin/index/', superuser_required(views.plugin_index), name='plugin_index'),
    path('plugin/', superuser_required(views.plugin), name='plugin'),
    path('plugout/index/', superuser_required(views.plugout_index), name='plugout_index'),
    path('plugout/backup/', superuser_required(views.plugout_backup), name='plugout_backup'),
    path('plugout/', superuser_required(views.plugout), name='plugout'),
    path('sendtestmail/', superuser_required(views.sendtestmailmanagers), name='sendtestmail'),
    # catch-all
    path('', views.index, name='index'),
]

handler500 = 'bots.views.server_error'
