from Estabelecimento import models
import json
from decimal import Decimal
from django.db.utils import IntegrityError, DataError
from django.utils.text import slugify

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

        cleaned_estabelecimento = {
            "id" : estabelecimento.get("cod_estabelecimento"),
            "nome" : estabelecimento.get("razao_social") if len(estabelecimento.get("razao_social")) > 0 else estabelecimento.get("nome"),
            # slug is auto generated
            "CNPJ_estabelecimento" : estabelecimento.get("cnpj"),
            "nome_responsavel" : estabelecimento.get("responsavel"),
            "CPF_responsavel" : estabelecimento.get("cpf_cnpj"),
            "telefone_contato_1" : estabelecimento.get("ddd_telefone") + estabelecimento.get("telefone"),
            "telefone_contato_2" : estabelecimento.get("ddd_celular") + estabelecimento.get("celular"),
            "email_contato" : estabelecimento.get("email"),
            "observacoes" : "Importado do Banco de Dados Legado.",
            "descricao" : estabelecimento.get("descricao"),
            "status_destaque" : True if estabelecimento.get("destaque") == 1 else False,
            "impulsionamentos" : estabelecimento.get("total_avaliacoes"),
            "nota" : estabelecimento.get("media"),
            "categoria" : None,
            "endereco_fiscal" : None,
            "endereco_comercial" : None,
            "dados_divulgacao" : None,
            "imagens_divulgacao" : None
        }

        try:
            fato = models.FatoEstabelecimento.objects.create(
                id = cleaned_estabelecimento.get("id"),
                nome = cleaned_estabelecimento.get("nome"),
                CNPJ_estabelecimento = cleaned_estabelecimento.get("CNPJ_estabelecimento"),
                nome_responsavel = cleaned_estabelecimento.get("nome_responsavel"),
                telefone_contato_1 = cleaned_estabelecimento.get("telefone_contato_1"),
                telefone_contato_2 = cleaned_estabelecimento.get("telefone_contato_2"),
                email_contato = cleaned_estabelecimento.get("email_contato"),
                observacoes = cleaned_estabelecimento.get("observacoes"),
                descricao = cleaned_estabelecimento.get("descricao"),
                status_destaque = cleaned_estabelecimento.get("status_destaque"),
                impulsionamento = cleaned_estabelecimento.get("impulsionamentos"),
                nota = Decimal(cleaned_estabelecimento.get("nota"))
            )

            created += 1

            print("FATO {} CREATED. {}/{} - {}".format(fato.id, created, total, slugify(fato.nome)))

        except:
            continue
