from django.contrib import admin
from django.db.models import Count
from . import models

# Register your models here.
@admin.register(models.Cidade)
class CidadeAdmin(admin.ModelAdmin):
    search_fields = ("cidade", "estado", )
    list_display = ("cidade", "estado", "pais", "estabelecimentos", )
    list_filter = ("pais", "estado", )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _estabelecimento_count = Count("endereco_cidade__estabelecimento_endereco_comercial", distinct=True)
        )
        return queryset

    def estabelecimentos(self, obj):
        return obj._estabelecimento_count

    estabelecimentos.admin_order_field = '-_estabelecimento_count'

@admin.register(models.Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ("nome", "categoria_pai__nome",)
    list_display = ("nome", "estabelecimentos", "categoria_pai",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _estabelecimento_count = Count("estabelecimentos_categorias", distinct=True)
        )
        return queryset

    def estabelecimentos(self, obj):
        return obj._estabelecimento_count

    estabelecimentos.admin_order_field = "-_estabelecimento_count"

@admin.register(models.FatoEstabelecimento)
class FatoAdmin(admin.ModelAdmin):
    search_fields = ("nome", "categoria__nome",)
    list_display = ("nome", "ativo",)
    list_filter = ("ativo", ) 
    filter_horizontal = ("categoria",)

@admin.register(models.DadosDivulgacao)
class DDivulgacaoAdmin(admin.ModelAdmin):
    search_fields = ("nome", "estabelecimento_dados_divulgacao__nome",)
    list_display = ("nome", )
    list_filter = ("estabelecimento_dados_divulgacao__ativo", )

@admin.register(models.Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    search_fields = ("estabelecimento_endereco_comercial__nome", "estabelecimento_endereco_fiscal__nome", "cidade__estado", "cidade__cidade", "logradouro", "bairro")
    list_display = ("__str__", "get_name", )
    list_filter = ("cidade__estado", )

    def get_name(self, obj):
        if obj.estabelecimento_endereco_comercial:
            nome = ", ".join(estabelecimento.nome for estabelecimento in obj.estabelecimento_endereco_comercial.all())
        elif estabelecimento_endereco_fiscal:
            nome = ", ".join(estabelecimento.nome for estabelecimento in obj.estabelecimento_endereco_fiscal.all())
        else:
            nome = "-"

        if nome == "":
            nome = "-"

        return nome

    get_name.short_description = "Estabelecimento"

@admin.register(models.Nota)
class FatoAdmin(admin.ModelAdmin):
    search_fields = ("estabelecimento__nome",)
    autocomplete_fields = ("estabelecimento", "usuario", )



#admin.site.register(models.Endereco)
admin.site.register(models.ImagensEstabelecimento)
admin.site.register(models.Impulsionamento)
#admin.site.register(models.Nota)
