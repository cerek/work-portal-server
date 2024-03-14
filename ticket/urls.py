from django.urls.conf import include, path
from rest_framework.routers import DefaultRouter
from ticket.views import TicketViewSet, TicketTypeViewSet, MyTicketViewSet, MyDeptTicketViewSet
from ticket.views import SelectBoxTicketTypeViewSet


router = DefaultRouter()
router.register(r'ticket', TicketViewSet, basename="ticket")
router.register(r'myticket', MyTicketViewSet, basename="myticket")
router.register(r'mydeptticket', MyDeptTicketViewSet, basename="mydept-ticket")
router.register(r'tickettype', TicketTypeViewSet, basename="ticket-type")

urlpatterns = [
    # path('ticket/kanban/', TicketKanbanViewSet.as_view(), name='ticket-kanban'),
    # path('ticket/report/', TicketReportViewSet.as_view(), name='ticket-report'),
    path('selectbox/tickettype/', SelectBoxTicketTypeViewSet.as_view(), name='select-ticket-type'),
    path('', include(router.urls)),
]
