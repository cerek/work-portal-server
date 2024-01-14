from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from menu.views import MenuViewSet, MenuGenerateListView


router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename="menu")

urlpatterns = [
    path("menu/generate/", MenuGenerateListView.as_view(), name="menu-generate"),
    path('', include(router.urls)),
]
