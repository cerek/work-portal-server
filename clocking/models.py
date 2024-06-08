from django.db import models
from employee.models import Employee
from location.models import Location


class ClockingMachine(models.Model):
    CLOCKING_MACHINE_TYPE = [
        (0, "Finger Print"),
        (1, "WebCam"),
        (2, "CardTap"),
    ]
    CLOCKING_MACHINE_STATUS_CHOICES = [
        (0, 'Suspend'),
        (1, 'Active'),
    ]
    clocking_machine_name = models.CharField(max_length=100)
    clocking_machine_status = models.SmallIntegerField(choices=CLOCKING_MACHINE_STATUS_CHOICES, default=1)
    # clocking_machine_ip = models.CharField(max_length=20, null=True, blank=True)
    clocking_machine_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    clocking_machine_type = models.SmallIntegerField(choices=CLOCKING_MACHINE_TYPE, default=0)
    clocking_machine_firmware_version = models.CharField(max_length=100, default='')
    clocking_machine_desc = models.TextField(default='')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clocking_machine_name}({self.get_clocking_machine_type_display()})"

    class Meta:
        ordering = ['-created_time']


class ClockingFingerRecord(models.Model):
    FINGER_CHOOICES = [
        (0, "Left Pinky Finger"),
        (1, "Left Ring Finger"),
        (2, "Left Middle Finger"),
        (3, "Left Index Finger"),
        (4, "Left Thumb"),
        (5, "Right Pinky Finger"),
        (6, "Right Ring Finger"),
        (7, "Right Middle Finger"),
        (8, "Right Index Finger"),
        (9, "Right Thumb"),
    ]
    finger_record_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    finger_record_machine = models.ManyToManyField('ClockingMachine')
    finger_record_position = models.SmallIntegerField()
    # finger_record_image = models.ImageField()
    finger_record_choose = models.SmallIntegerField(choices=FINGER_CHOOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']


class ClockingRecord(models.Model):
    IS_EIDT_CHOICES = [
        (0, "No"),
        (1, "Yes"),
    ]
    clocking_record_employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    clocking_record_datetime = models.DateTimeField()
    clocking_record_is_edit = models.SmallIntegerField(choices=IS_EIDT_CHOICES, default=0)
    clocking_record_machine = models.ForeignKey("ClockingMachine", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']
        permissions = [
            ('manager_clocking_record_change', 'Can edit clocking record data'),
            ('view_timecard_personal', 'Can view timecard personal'),
            ('view_timecard_check', 'Can view timecard on calendar'),
        ]
