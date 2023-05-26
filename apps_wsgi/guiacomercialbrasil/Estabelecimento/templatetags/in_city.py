from django import template
from django.db.models import Q

register = template.Library()

@register.filter
def in_city(category, city):
    #return '{} - {}'.format(category.subcategorias_validas(), city)
    ''' Returns True if there are Estabelecimentos of given Category in Given City '''
    if category.subcategorias_validas().count() > 0:
        if any([subcategory.estabelecimentos_categorias.filter(Q(endereco_comercial__cidade = city) | Q(alcance_nacional = True)).filter(ativo = True).count() > 0 for subcategory in category.subcategorias_validas()]):
            return True
        else:
            return False

    else: 
        if category.estabelecimentos_categorias.filter(Q(endereco_comercial__cidade = city) | Q(alcance_nacional = True)).filter(ativo = True).count() > 0:
            return True
        else:
            return False
