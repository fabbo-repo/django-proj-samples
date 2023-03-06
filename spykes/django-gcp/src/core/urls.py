
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

handler404 = 'core.views.not_found_view'
handler500 = 'core.views.error_view'
handler403 = 'core.views.permission_denied_view'
handler400 = 'core.views.bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    # For django.contrib.auth.urls, it includes:
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]