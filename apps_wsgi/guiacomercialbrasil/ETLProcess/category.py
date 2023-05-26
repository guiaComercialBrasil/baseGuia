from ETLProcess import JSONParser, FTPTransfer
from Estabelecimento import models
from django.core.files import File
import json

OLD_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/OLDDATABASE"
NEW_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/NEWDATABASE"

TABLES = {
    "estabelecimentos" : "guiacome_site_table_estabelecimento.json",
    "categorias" : "guiacome_site_table_categoria.json",
    "cidades" : "guiacome_site_table_cidade.json",
    "estabelecimento_cidades" : "guiacome_site_table_estabelecimento_cidades.json",
    "galeria" : "guiacome_site_table_galeria.json",
    "estabelecimento_categoria" : "guiacome_site_table_estabelecimento_categoria.json"
}

total = models.FatoEstabelecimento.objects.all().count()
done = 0
failed = 0

with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimento_categoria")), "r", encoding="utf-8") as inputfile:
    with open("{}/{}".format(OLD_DATABASE, TABLES.get("categorias")), "r", encoding="utf-8") as inputfile2:
    
        data = json.load(inputfile).get("data")
        categorias = json.load(inputfile2).get("data")

        for categoria_cartao in data:

            for categoria in categorias:
                if categoria.get("cod_categoria") == categoria_cartao.get("cod_categoria"):
                    categ = categoria.get("categoria")
                    break

            try:
                estabelecimento = models.FatoEstabelecimento.objects.get(id = categoria_cartao.get("cod_estabelecimento"))
                categoria = models.Categoria.objects.get(nome = categ)
                
                estabelecimento.categoria.add(categoria)
                estabelecimento.save()
                
                done += 1
                print("{} - DONE ({}/{})".format(estabelecimento.id, done, total))
                continue

            except Exception as e:
                failed += 1
                print("{} - FAILED ({}/{}): {}".format(estabelecimento.id, failed, total, e))
                continue











#with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile1:
#    with open("{}/{}".format(OLD_DATABASE, TABLES.get("categoria_cartao")), "r", encoding="utf-8") as inputfile2:
#        
#        estabelecimentos = json.load(inputfile1).get("data")
#        categorias_cartao = json.load(inputfile2).get("data")
#
#        for estabelecimento in estabelecimentos:
#            cod_estabelecimento = estabelecimento.get("cod_estabelecimento")
#
#            for categoria_cartao in categorias_cartao:
#                if categoria_cartao.get("cod_categoria_cartao") == cod_estabelecimento:
#                    categoria = categoria_cartao.get("categoria")
#                    break
#            
#            estab_obj = models.FatoEstabelecimento.objects.get(id = cod_estabelecimento)
#            categ_obj = models.Categoria.objects.get(nome = categoria)
#
#            estab_obj.categoria.add(categ_obj)
#            estab_obj.save()
#            print()
