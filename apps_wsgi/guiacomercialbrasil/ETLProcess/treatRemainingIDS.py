from Estabelecimento import models
import json
from decimal import Decimal
from django.db.utils import IntegrityError
from django.utils.text import slugify

OLD_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/OLDDATABASE"
NEW_DATABASE = r"/home/agendadecartoes/apps_wsgi/guiacomercialbrasil/ETLProcess/NEWDATABASE"

rids = [
    "261", "2533", "2534", "2543", "2556", "2588", "2607", "2615", "2620", "2623", "2635", "2677", "2713", "2764",
    "2828", "2829", "2862", "2884", "2888", "2893", "3123", "3168", "3179", "3180", "3197", "3237", "3238", "3245",
    "3248", "3251", "3253", "3281", "3329", "3340", "3346", "3347", "3353", "3354", "3489", "3500", "3515", "3525",
    "3530", "3551", "3554", "3565", "3568", "3590", "3593", "3594", "3596", "3601", "3602", "3606", "3615", "3618",
    "3640", "3641", "3642", "3646", "3649", "3659", "3664", "3667", "3672", "3673", "3674", "3678", "3683", "3692",
    "3693", "3694", "3695", "3715", "3716", "3726", "3735", "3737", "3756", "3758", "3761", "3777", "3784", "3785",
    "4038", "4043", "4054", "4083", "4212", "4232", "4233", "4240", "4241", "4244", "4245", "4246", "4248", "4252",
    "4253", "4255", "4263", "4265", "4282"
]





TABLES = {
    "estabelecimentos" : "guiacome_site_table_estabelecimento.json",
    "categorias" : "guiacome_site_table_categoria.json",
    "cidades" : "guiacome_site_table_cidade.json",
    "estabelecimento_cidades" : "guiacome_site_table_estabelecimento_cidades.json",
    "galeria" : "guiacome_site_table_galeria.json"
}

with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as file:
    data = json.load(file).get("data")
    
    for estabelecimento in data:
        if estabelecimento.get("cod_estabelecimento") in rids:
        
            rids.pop(rids.index(estabelecimento.get("cod_estabelecimento")))
        
            try:
                cpf_cnpj = estabelecimento.get("cpf_cnpj") if len(estabelecimento["cpf_cnpj"]) < 14 else None
            except TypeError:
                cpf_cnpj = None

            try:
                nota = Decimal(cleaned_estabelecimento.get("nota"))
            except Exception:
                nota = 3

            cleaned_estabelecimento = {
                "id" : estabelecimento.get("cod_estabelecimento"),
                "nome" : estabelecimento.get("razao_social") + "-" + estabelecimento.get("cod_estabelecimento") if len(estabelecimento.get("razao_social")) > 1 else estabelecimento.get("nome") + "-" + estabelecimento.get("cod_estabelecimento"),
                # slug is auto generated
                "CNPJ_estabelecimento" : estabelecimento.get("cnpj"),
                "nome_responsavel" : estabelecimento.get("responsavel"),
                "CPF_responsavel" : cpf_cnpj,
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
                    nota = nota
                )
            except Exception as e:
                print("{}. {} ({}) - {}".format(estabelecimento.get("cod_estabelecimento"), slugify(estabelecimento.get("nome")), len(slugify(estabelecimento.get("nome"))), e))