from django.contrib import admin
from orimgasapp.models import Company, Position, Instruction, PositionInstruction


class companyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_id', 'manager')
    search_fields = ('name', 'company_id', 'manager')



class positionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    search_fields = ('name', 'company')

class instructionAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    search_fields = ('name', 'company')

class positionInstructionAdmin(admin.ModelAdmin):
    list_display = ('position', 'display_instructions')
    search_fields = ('position', 'display_instructions')


#admin.site.register(RegularUser)
#admin.site.register(SupervisorUser)
admin.site.register(Company, companyAdmin)
admin.site.register(Position, positionAdmin)
admin.site.register(Instruction, instructionAdmin)
admin.site.register(PositionInstruction, positionInstructionAdmin)
