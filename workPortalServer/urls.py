from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Third-Party URL
    path('auth/', include('dj_rest_auth.urls')),

    # Self-build app URL
    path('', include('location.urls')),
    path('', include('department.urls')),
    path('', include('employee.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)