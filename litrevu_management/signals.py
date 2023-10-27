import os
from litrevu_management.models import Ticket
from django.dispatch import receiver
from django.db.models.signals import pre_delete


@receiver(pre_delete, sender=Ticket)
def delete_ticket_image(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
