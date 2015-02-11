from django.contrib import admin
from plato.models import *


def make_inactif(modeladmin, request, queryset):
	queryset.update(actif=False)

class UserAdmin(admin.ModelAdmin):
	list_display = ['nm_person', 'fstnm_person', 'status', 'login', 'id_boss', 'actif']
	ordering= ['-actif','nm_person']
	actions = [make_inactif]
admin.site.register(User,UserAdmin)

admin.site.register(Group)
admin.site.register(File)
admin.site.register(EnsFile)
admin.site.register(Page)
admin.site.register(Tool)
admin.site.register(KW)

admin.site.register(Demo)
admin.site.register(Type_ES)
admin.site.register(ES_demo)
admin.site.register(Param_demo)
admin.site.register(DemoExample)




