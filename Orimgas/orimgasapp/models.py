from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_init
from django.dispatch import receiver



class Company(models.Model):
    name = models.CharField(max_length=100)
    company_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    manager = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instruction(models.Model):
    company = models.ForeignKey(Company, 
                                verbose_name=_("company"), 
                                on_delete=models.CASCADE,
                                related_name='instructions'
                                )
    name = models.CharField(max_length=100)
    periodity = models.DateField(_("periodicity"), default=None, blank=True, null=True)
    pdf = models.FileField(upload_to='instructions')

    def __str__(self):
        return f"{self.company} {self.name}"


class Position(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company,
                                verbose_name=_("company"), 
                                on_delete=models.CASCADE,
                                related_name='positions'
                                )

    def __str__(self):
        return f"{self.company} {self.name}"



def validate_position_instruction(instance):
    for instruction in instance.instruction.all():
        if instance.position.company != instruction.company:
            raise ValidationError("Position's company doesn't match the company of the instruction.")

def delete_if_error_raised(instance):
    try:
        validate_position_instruction(instance)
    except ValidationError:
        # If ValidationError is raised, delete the object
        instance.delete()
        raise 

class PositionInstruction(models.Model):
    position = models.ForeignKey(Position, 
                                 verbose_name=_("position"), 
                                 on_delete=models.CASCADE,
                                 related_name='position_instruction'
                                 )
    instruction = models.ManyToManyField(Instruction,
                                        verbose_name=_("instruction"),
                                        related_name='position_instruction',
                                        )

    def display_instructions(self):
        return ', '.join([instruction.name for instruction in self.instruction.all()])
    display_instructions.short_description = _('instructions')

@receiver(post_init, sender=PositionInstruction)
def handle_position_instruction_save(sender, instance, **kwargs):
    for instruction in instance.instruction.all():
        if instance.position.company != instruction.company:
            instance.delete()
            raise ValidationError("Position's company doesn't match the company of the instruction.")
