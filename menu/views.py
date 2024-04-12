from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from menu.models import Menu
from menu.serializers import MenuSerializer
from utils.public_permission import ExtendViewPermission
from utils.public_pagination import StandardResultsSetPagination


class MenuViewSet(viewsets.ModelViewSet):
    permission_classes = [ExtendViewPermission]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filterset_fields = ['menu_name', 'menu_show', 'menu_url']
    search_fields = ['menu_name', 'menu_show', 'menu_url']
    pagination_class = StandardResultsSetPagination

    def destroy(self, request, *args, **kwargs):
        delete_obj = self.get_object()
        obj_serializer = self.get_serializer(self.get_object()).data

        try:
            delete_obj.delete()
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_400_BAD_REQUEST)

        # Return the deleted object to client.
        return Response(obj_serializer, status=status.HTTP_200_OK)


class MenuGenerateListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        employee = request.user.employee

        ret_menu_list = []
        tmp_dict = {}
        public_menu_dict = {"label": "Public Menu", "items": []}
        it_menu_dict = {"label": "IT Menu", "items": []}
        hr_menu_dict = {"label": "Human Resource Menu", "items": []}
        accounting_menu_dict = {"label": "Accounting Menu", "items": []}
        inventory_menu_dict = {"label": "Inventory Menu", "items": []}
        admin_menu_dict = {"label": "Admin Menu", "items": []}

        hr_menu_context = ['human_resource_manager', 'schedule_manager', 'performance_manager', 'announcement_manager',]
        it_menu_context = ['asset', 'ticket_system',]
        accounting_menu_context = []
        inventory_menu_context = ['warehouse_manager',]
        admin_menu_context = ['permission_manager', 'menu_manager', 'static_manager', 'logging_manager', 'task_manager']


        # Retrieve Public Menu, Only get the active public menu list
        pub_menu_qs = Menu.objects.filter(permission_id__in=employee.gain_permission()).filter(menu_type=0).filter(menu_status=1).order_by('menu_priority')
        for pm in pub_menu_qs:
            if pm.menu_need_id == 1:
                to_menu_url = f'{pm.menu_url}/{employee.id}'
            else:
                to_menu_url = pm.menu_url
            public_menu_dict["items"].append({"label": pm.menu_show, "icon": pm.menu_icon, "to": to_menu_url})

        # Retrieve Employee Menu, base on Permission
        emp_menu_qs = Menu.objects.filter(permission_id__in=employee.gain_permission()).filter(permission_id__name__icontains='view').exclude(menu_type=0).filter(menu_status=1).order_by('menu_priority')

        for m in emp_menu_qs:
            # For Level 1
            if m.menu_parent_id is None and m.menu_type == 2:
                if m.menu_category == 1:
                    it_menu_dict["items"].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
                elif m.menu_category == 2:
                    hr_menu_dict["items"].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
                elif m.menu_category == 3:
                    accounting_menu_dict["items"].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
                elif m.menu_category == 4:
                    inventory_menu_dict["items"].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
                elif m.menu_category == 10:
                    admin_menu_dict["items"].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
            # For Level 2
            elif m.menu_parent_id is not None and m.menu_type == 3:
                parent_menu = Menu.objects.get(id=m.menu_parent_id_id)
                if parent_menu.menu_name not in tmp_dict:
                    parent_menu_dict = {"label": parent_menu.menu_show, "icon": parent_menu.menu_icon, "to": parent_menu.menu_url}
                    tmp_dict[parent_menu.menu_name] = parent_menu_dict
                    tmp_dict[parent_menu.menu_name]['items'] = []
                    tmp_dict[parent_menu.menu_name]['items'].append({"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url})
                else:
                    m_dict = {"label": m.menu_show, "icon": m.menu_icon, "to": m.menu_url}
                    tmp_dict[parent_menu.menu_name]['items'].append(m_dict)

        for k in tmp_dict:
            if k in hr_menu_context:
                hr_menu_dict["items"].append(tmp_dict[k])
            elif k in it_menu_context:
                it_menu_dict["items"].append(tmp_dict[k])
            elif k in accounting_menu_context:
                accounting_menu_dict["items"].append(tmp_dict[k])
            elif k in inventory_menu_context:
                inventory_menu_dict["items"].append(tmp_dict[k])
            elif k in admin_menu_context:
                admin_menu_dict["items"].append(tmp_dict[k])

        ret_menu_list.append(public_menu_dict)
        if len(hr_menu_dict["items"]) !=0:
            ret_menu_list.append(hr_menu_dict)
        if len(it_menu_dict["items"]) != 0:
            ret_menu_list.append(it_menu_dict)
        if len(accounting_menu_dict["items"]) != 0:
            ret_menu_list.append.extend(accounting_menu_dict)
        if len(inventory_menu_dict["items"]) != 0:
            ret_menu_list.append(inventory_menu_dict)
        if len(admin_menu_dict["items"]) != 0:
            ret_menu_list.append(admin_menu_dict)

        return Response(ret_menu_list)