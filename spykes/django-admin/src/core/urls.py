from django.contrib import admin
from django.urls import path

handler404 = 'core.views.not_found_view'
handler500 = 'core.views.error_view'
handler403 = 'core.views.permission_denied_view'
handler400 = 'core.views.bad_request_view'

urlpatterns = [
    path('admin/', admin.site.urls),
]
