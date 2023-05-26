from Estabelecimento import models
import json
from decimal import Decimal
from django.db.utils import IntegrityError
from ETLProcess import JSONParser


OLD_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/OLDDATABASE"
NEW_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/NEWDATABASE"

TABLES = {
    "estabelecimentos" : "guiacome_site_table_estabelecimento.json",
    "categorias" : "guiacome_site_table_categoria.json",
    "cidades" : "guiacome_site_table_cidade.json",
    "estabelecimento_cidades" : "guiacome_site_table_estabelecimento_cidades.json",
    "galeria" : "guiacome_site_table_galeria.json"
}

# Open file stream as read
input_estab = open(OLD_DATABASE + "/" + TABLES.get("estabelecimentos"), "r", encoding = "utf-8")
input_cidades = open(OLD_DATABASE + "/" + TABLES.get("cidades"), "r", encoding = "utf-8")
input_estab_cidades = open(OLD_DATABASE + "/" + TABLES.get("estabelecimento_cidades"), "r", encoding = "utf-8")





# UPLOAD CITIES
#created = 0
# for cidade in JSONParser.cidade(input_cidades):
#     if cidade.get("estado") in ["SP", "RJ"]:
#         models.Cidade.objects.create(id = cidade.get("id"), pais = cidade.get("pais"), estado = cidade.get("estado"), cidade = cidade.get("cidade"))
#         created += 1
#         print("{} CREATED ({})".format(cidade.get("cidade"), created))
#     else:
#         print("WRONG UF: ", cidade.get("uf"))
# 

['Mairiporã', 'Amparo', 'Rio Claro', 'Santa Isabel']

# UPLOAD ADDRESSES
data = JSONParser.endereco(input_estab, input_cidades, input_estab_cidades)
total, created = len(data), 0

for endereco in data:
# ADDR TREATMENT
    
        estabelecimento = models.FatoEstabelecimento.objects.get(id = endereco.get("cod_estabelecimento"))
        
        if not estabelecimento.endereco_comercial:
            try:
                cidade = models.Cidade.objects.get(cidade = endereco.get("nome_cidade"))
                addr = models.Endereco.objects.create(
                    cidade = cidade,
                    bairro = endereco.get("bairro"),
                    logradouro = endereco.get("logradouro"),
                    numero = endereco.get("numero")
                )

                estabelecimento.endereco_comercial = addr
                estabelecimento.endereco_fiscal = addr

                estabelecimento.save()

                created += 1

                print("({}/{}) - ESTABELECIMENTO: {}, ENDERECO: {}".format(created, total, estabelecimento.id, addr.id))

            except Exception as e:

                print("({}) {}/{} - {}".format(endereco.get("cod_estabelecimento"), endereco.get("nome_cidade"), endereco.get("estado"), e))
        

# FULL ADDR INCLUSION
#    try:
#        estabelecimento = models.FatoEstabelecimento.objects.get(id = endereco.get("cod_estabelecimento"))
#        cidade = models.Cidade.objects.get(cidade = endereco.get("nome_cidade"))
#        addr = models.Endereco.objects.create(
#            cidade = cidade,
#            bairro = endereco.get("bairro"),
#            logradouro = endereco.get("logradouro"),
#            numero = endereco.get("numero")
#        )
#        
#        estabelecimento.endereco_comercial = addr
#        estabelecimento.endereco_fiscal = addr
#
#        estabelecimento.save()
#
#        created += 1
#
#        print("({}/{}) - ESTABELECIMENTO: {}, ENDERECO: {}".format(created, total, estabelecimento.id, addr.id))
#
#    except Exception as e:
#
#        print("({}) {}/{} - {}".format(endereco.get("cod_estabelecimento"), endereco.get("nome_cidade"), endereco.get("estado"), e))


# Close file stream
input_estab.close()
input_cidades.close()
input_estab_cidades.close()