from django.shortcuts import redirect
from django.db.utils import IntegrityError
from django.urls import get_resolver
from Customizacao.models import Customizacao

# Create your views here.
def syncPagesCustomization(request, *args, **kwargs):
    paginas = [x for x in get_resolver().reverse_dict.keys() if type(x)  == str]
    customizacoes = Customizacao.objects.all()

    if any([customizacao.pagina not in paginas for customizacao in customizacoes]):
        for customizacao in customizacoes:
            if customizacao not in paginas:
                customizacao.delete()

    for pagina in paginas:
        try:
            Customizacao.objects.create(pagina = pagina)
        except IntegrityError:
            pass

    return redirect(request.META.get("HTTP_REFERER", "/admin"))