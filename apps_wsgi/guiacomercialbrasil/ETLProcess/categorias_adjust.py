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

with open("{}/{}".format(OLD_DATABASE, TABLES.get("categorias")), "r", encoding="utf-8") as inputfile:
    data = json.load(inputfile).get("data")

transfer = FTPTransfer.Transfer()
total = models.Categoria.objects.all().count()
done_descricao = 0
done_imagem = 0
failed_descricao = 0
failed_imagem = 0

for categoria in models.Categoria.objects.all():

    for d in data:
        if d.get("categoria") == categoria.nome:
            try:
                if d.get("descritivos"):
                    try:
                        categoria.descrição = d.get("descritivos")
                        categoria.save()
                        done_descricao += 1
                        print("{} DONE DESCRIÇÃO ({}/{})".format(categoria.id, done_descricao, total))
                    except Exception as e:
                        failed_descricao += 1
                        print("{} FAILED DESCRIÇÃO ({}/{}) - {}".format(categoria.id, failed_descricao, total, e))

                transfer.get_remotefile(filename = d.get("imagem"))
                categoria.imagem.save(d.get("imagem"), File(open(d.get("imagem"), "rb")))
                transfer.remove_localfile(filename = d.get("imagem"))
                
                done_imagem += 1
                print("{} DONE IMAGEM ({}/{})".format(categoria.id, done_imagem, total))


            except Exception as e:
                failed_imagem += 1
                print("{} FAILED IMAGEM ({}/{})".format(categoria.id, failed_imagem, total))
            
            break
        
        
    
transfer.disconnect()
print("RESULT: TOTAL{}\n{} DESCRIÇÃO SUCCESS\n{} DESCRIÇÃO ERROR\n{} IMAGEM SUCCESS\n{} IMAGEM ERROR".format(total, done_descricao, failed_descricao, done_imagem, failed_imagem))