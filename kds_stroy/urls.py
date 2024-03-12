from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from kds_stroy import settings
from users.views import RegistrationView
from main.views import MainView

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path('verification/', include('verify_email.urls')),
    path("auth/registration/", RegistrationView.as_view(), name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("profile/", include("users.urls")),
    path("orders/", include("orders.urls")),
    path("news/", include("news.urls")),
    path("privacy/",
         TemplateView.as_view(template_name="pages/personal_terms.html"),
         name="personal_info_terms"),
]

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += (path('debug/', include(debug_toolbar.urls)),)
