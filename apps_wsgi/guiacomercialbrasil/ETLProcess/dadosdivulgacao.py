from Estabelecimento import models
import json
from decimal import Decimal
from django.db.utils import IntegrityError

OLD_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/OLDDATABASE"
NEW_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/NEWDATABASE"

TABLES = {
    "estabelecimentos" : "guiacome_site_table_estabelecimento.json",
    "categorias" : "guiacome_site_table_categoria.json",
    "cidades" : "guiacome_site_table_cidade.json",
    "estabelecimento_cidades" : "guiacome_site_table_estabelecimento_cidades.json",
    "galeria" : "guiacome_site_table_galeria.json"
}


with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as file:
    data = json.load(file).get("data")

    total = len(data)
    created = 0

    for estabelecimento in data:
        cleaned_dd = {
            "nome" : "temp",
            "descricao" : estabelecimento.get("descricao"),
            "telefone" : None,
            "whatsapp" : None,
            "site" : estabelecimento.get("site"),
            "instagram" : None,
            "facebook" : None,
            "twitter" : None,
            "linkedin" : None
        }

        try:
            dd = models.DadosDivulgacao(
                nome = cleaned_dd.get("nome"), descricao = cleaned_dd.get("descricao"), site = cleaned_dd.get("site")
                )
            dd.save()
            estab = models.FatoEstabelecimento.objects.get(id = estabelecimento.get("cod_estabelecimento"))
            estab.dados_divulgacao = dd
            estab.save()
            dd.nome = None
            dd.save()

            created += 1

            print("{}/{}".format(created, total))
            
        except Exception as e:
            if estabelecimento.get("cod_estabelecimento") == "4063":
                dd = models.DadosDivulgacao(
                    nome = cleaned_dd.get("nome"), descricao = "Importado do Banco de Dados Legado.", site = cleaned_dd.get("site")
                )
                dd.save()
                estab = models.FatoEstabelecimento.objects.get(id = estabelecimento.get("cod_estabelecimento"))
                estab.dados_divulgacao = dd
                estab.save()
                dd.nome = None
                dd.save()

                created += 1

                print("{}/{}".format(created, total))

                continue

            print("{}. {} - {}".format(estabelecimento.get("cod_estabelecimento"), cleaned_dd.get("nome"), e))