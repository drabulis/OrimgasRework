from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from .models import PositionInstruction
from django.core.exceptions import ValidationError

@receiver(post_init, sender=PositionInstruction)
def handle_position_instruction_save(sender, instance, **kwargs):
        for instruction in instance.instruction.all():
            if instance.position.company != instruction.company:
                instance.delete()
                raise ValidationError("Position's company doesn't match the company of the instruction.")
