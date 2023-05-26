"""GuiaComercialBrasil URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import Estabelecimento.views
import Customizacao.views

handler404 = Estabelecimento.views.handler404
handler500 = Estabelecimento.views.handler500

urlpatterns = [
    ## REGULAR
    path('', Estabelecimento.views.HomeView.as_view(), name = "home"),
    path('admin/', admin.site.urls),
    path('estabelecimento/', include('Estabelecimento.urls')),
    path('categoria/<slug:categoria>', Estabelecimento.views.CategoryView.as_view(), name = "estab_categoria"),
    path('contato/', Estabelecimento.views.ContactView.as_view(), name = "contact"),
    path('busca/', Estabelecimento.views.SearchView.as_view(), name = "search"),
    path('quem-somos/', Estabelecimento.views.WhoAreWeView.as_view(), name = "quem_somos"),
    path('telefones/', Estabelecimento.views.ContactNumbersView.as_view(), name = "telefones_uteis"),


    ## UTILITY
    path('mudar-cidade/<int:city_id>', Estabelecimento.views.changeCity, name = "change_city"),
    path('mudar-cidade/<slug:city>', Estabelecimento.views.changeCity, name = "change_city_slugified"),
    path('sync-pages-customization/', Customizacao.views.syncPagesCustomization, name = "sync_customizacao"),

    ### AJAX
    path('ajax/boost/', Estabelecimento.views.boost, name = "ajax-boost"),
    path('ajax/rate/', Estabelecimento.views.rate, name = "ajax-rate"),
    path('ajax/autocomplete-city/', Estabelecimento.views.autocompleteCity, name = "ajax_autocomplete_city"),
    
    
    path('<slug:city>', Estabelecimento.views.HomeView.as_view(), name = "cidade"),
    
]
