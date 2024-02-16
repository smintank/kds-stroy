from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from kds_stroy import settings
from users.views import register

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("admin/", admin.site.urls),
    path('verification/', include('verify_email.urls')),
    path("auth/registration/", register, name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("users/", include("users.urls")),
    path("orders/", include("orders.urls")),
    path("news/", include("news.urls")),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about"
    ),
]

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += (path('debug/', include(debug_toolbar.urls)),)
