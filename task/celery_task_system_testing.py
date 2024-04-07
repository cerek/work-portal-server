from celery import shared_task

from time import sleep

@shared_task
def system_task_testing():
    for i in range(11):
        print(i)
        sleep(1)
    return "Task Complete!"

