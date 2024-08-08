from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from kds_stroy import settings
from main.views import MainView, TermsView, handler404
from users.views import RegistrationView

urlpatterns = [
    path("", MainView.as_view(), name="home"),
    path("terms/", TermsView.as_view(), name="personal_info_terms"),
    path("admin/", admin.site.urls),
    path("verification/", include("verify_email.urls")),
    path("auth/registration/",
         RegistrationView.as_view(),
         name="registration"),
    path("auth/", include("django.contrib.auth.urls")),
    path("profile/", include("users.urls")),
    path("orders/", include("orders.urls")),
    path("news/", include("news.urls")),
    path("subs/", include("ads_mailing.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = handler404
