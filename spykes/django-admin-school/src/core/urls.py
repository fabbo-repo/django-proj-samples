from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

handler404 = "core.views.not_found_view"
handler500 = "core.views.error_view"
handler403 = "core.views.permission_denied_view"
handler400 = "core.views.bad_request_view"

# Text to put at the end of each page's <title>.
admin.site.site_header = "Admin School App"
# Text to put in each page's <h1> (and above login form).
admin.site.site_title = "School App"
# Text to put at the top of the admin index page.
admin.site.index_title = "Admin site"

urlpatterns = [
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
