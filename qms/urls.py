from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from qms.views import QMSServiceTypeViewSet, QMSTicketViewSet, QMSTicketTemplateViewSet

router = DefaultRouter()
router.register(r'qmsservice', QMSServiceTypeViewSet, basename="qms-service")
router.register(r'qmsticket', QMSTicketViewSet, basename="qms-ticket")
router.register(r'qmstickettemplate', QMSTicketTemplateViewSet, basename="qms-ticket-template")

urlpatterns = [
    path('', include(router.urls)),
]
