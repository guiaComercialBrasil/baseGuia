from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Customizacao)
class CustomizacaoAdmin(admin.ModelAdmin):

    fields = ("pagina", "texto_1", "texto_2")
    readonly_fields = ("pagina",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
