from django.db import models
from employee.models import Employee
from department.models import Department
from upload.models import Upload


class Ticket(models.Model):
    STATUS_CHOICES = [
        (0, 'New'),
        (1, 'In progress'),
        (2, 'On hold'),
        (3, 'Finished'),
        (4, 'Rejected'),
        (5, 'Closed'),
    ]
    # RATING_CHOICES = [(x,x) for x in range(0,6)]
    ticket_title = models.CharField(max_length=200, null=False, blank=False)
    ticket_creator = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='ticket_creator')
    ticket_assigner = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='ticket_assigner')
    ticket_assign_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=False, blank=False)
    ticket_description = models.TextField(null=False, blank=False)
    ticket_solution = models.TextField(null=True, blank=True)
    ticket_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0)
    ticket_type = models.ForeignKey('TicketType', on_delete=models.DO_NOTHING)
    ticket_attachment = models.ManyToManyField(Upload, null=True, blank=True)
    ticket_final_time = models.DateTimeField(null=True, blank=True)
    # ticket_rating = models.SmallIntegerField(choices=RATING_CHOICES, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def ticket_duration(self):
        if self.ticket_final_time == None:
            return 0
        else:
            duration = self.ticket_final_time - self.created_time
            return duration.seconds

    class Meta:
        ordering = ['-created_time']
        permissions = [
            ('view_ticket_kanban', 'Can view ticket kanban'),
            ('view_ticket_report', 'Can view ticket report'),
            ('view_ticket_personal', 'Can view ticket personal'),
            ('update_ticket_department', 'Can update own department tickets'),
        ]

    def __str__(self):
        return self.ticket_title


class TicketType(models.Model):
    ticket_type_name = models.CharField(max_length=100, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticket_type_name

    class Meta:
        ordering = ['-created_time']