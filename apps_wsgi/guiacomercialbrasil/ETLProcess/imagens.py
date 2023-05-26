from Estabelecimento import models
import json
from decimal import Decimal
from django.db.utils import IntegrityError
from ETLProcess import JSONParser, FTPTransfer
from django.core.files import File


OLD_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/OLDDATABASE"
NEW_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/NEWDATABASE"

TABLES = {
    "estabelecimentos" : "guiacome_site_table_estabelecimento.json",
    "categorias" : "guiacome_site_table_categoria.json",
    "cidades" : "guiacome_site_table_cidade.json",
    "estabelecimento_cidades" : "guiacome_site_table_estabelecimento_cidades.json",
    "galeria" : "guiacome_site_table_galeria.json"
}


# IMAGENS ESTABELECIMENTO
with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile1:
    with open("{}/{}".format(OLD_DATABASE, TABLES.get("galeria")), "r", encoding="utf-8") as inputfile2:
        transfer = FTPTransfer.Transfer()
        
        data = JSONParser.imagens_estabelecimento(inputfile1, inputfile2)
        total = len(data)
        created = 0

        for estabelecimento in data:
            
            fato = models.FatoEstabelecimento.objects.get(id = estabelecimento.get("cod_estabelecimento"))

            if fato.imagens_divulgacao:
                continue
            
            
            # GET FROM LOCAL REP
            print(estabelecimento.get("imagem_cartao"))
            try:
                imagensestabelecimento = models.ImagensEstabelecimento(
                    nome_estabelecimento = estabelecimento.get("nome_estabelecimento")
                )

                

                if estabelecimento.get("imagem_cartao"):
                    

                    imagensestabelecimento.imagem_cartao.save(
                        estabelecimento.get("imagem_cartao"),
                        File(open(NEW_DATABASE + "/RESFILES/" + estabelecimento.get("imagem_cartao"), "rb"))
                    )
                    
                    created += 1
                    print("ESTABELECIMENTO: {} ({}/{})".format(estabelecimento.get("cod_estabelecimento"), created, total))
                    

                    # LINK TO ESTAB


                    fato.imagens_divulgacao = imagensestabelecimento
                    fato.save()


            
            


            # GET FROM FTP
            #try:
            #    imagensestabelecimento = models.ImagensEstabelecimento(
            #        nome_estabelecimento = estabelecimento.get("nome_estabelecimento")
            #    )
#
            #    created += 1
#
            #    print("ESTABELECIMENTO: {} ({}/{})".format(estabelecimento.get("cod_estabelecimento"), created, total))
#
            #    if estabelecimento.get("imagem_cartao"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_cartao"))
#
            #        imagensestabelecimento.imagem_cartao.save(
            #            estabelecimento.get("imagem_cartao"),
            #            File(open(estabelecimento.get("imagem_cartao"), "rb"))
            #        )
#
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_cartao"))
#
            #        # LINK TO ESTAB
            #        
            #        
            #        fato.imagens_divulgacao = imagensestabelecimento
            #        fato.save()
#
#
            #    if estabelecimento.get("imagem_1"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_1"))
#
            #        imagensestabelecimento.imagem_1.save(
            #            estabelecimento.get("imagem_1"),
            #            File(open(estabelecimento.get("imagem_1"), "rb"))
            #        )
            #        
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_1"))
            #    else:
            #        continue
#
            #    if estabelecimento.get("imagem_2"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_2"))
#
            #        imagensestabelecimento.imagem_2.save(
            #            estabelecimento.get("imagem_2"),
            #            File(open(estabelecimento.get("imagem_2"), "rb"))
            #        )
            #        
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_2"))
            #    else:
            #        continue
#
            #    if estabelecimento.get("imagem_3"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_3"))
#
            #        imagensestabelecimento.imagem_3.save(
            #            estabelecimento.get("imagem_3"),
            #            File(open(estabelecimento.get("imagem_3"), "rb"))
            #        )
            #        
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_3"))
            #    else:
            #        continue
#
            #    if estabelecimento.get("imagem_4"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_4"))
#
            #        imagensestabelecimento.imagem_4.save(
            #            estabelecimento.get("imagem_4"),
            #            File(open(estabelecimento.get("imagem_4"), "rb"))
            #        )
#
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_4"))
            #    else:
            #        continue
#
            #    if estabelecimento.get("imagem_cartao"):
            #        transfer.get_remotefile(filename = estabelecimento.get("imagem_cartao"))
#
            #        imagensestabelecimento.imagem_cartao.save(
            #            estabelecimento.get("imagem_cartao"),
            #            File(open(estabelecimento.get("imagem_cartao"), "rb"))
            #        )
#
            #        transfer.remove_localfile(filename = estabelecimento.get("imagem_cartao"))
            #    else:
            #        continue
            except Exception as e:
                print("ESTABELECIMENTO: {} - {}".format(estabelecimento.get("cod_estabelecimento"), e))