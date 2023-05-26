

# CIDADES
with open("{}/{}".format(OLD_DATABASE, TABLES.get("cidades")), "r", encoding="utf-8") as inputfile:
    for cidade in JSONParser.cidade(inputfile):
        models.Cidade.objects.create(id = cidade.get("id"), pais = cidade.get("pais"), estado = cidade.get("estado"), cidade = cidade.get("cidade"))
        
# CATEGORIAS
with open("{}/{}".format(OLD_DATABASE, TABLES.get("categorias")), "r", encoding="utf-8") as inputfile:
    for categoria in JSONParser.categoria(inputfile):
        models.Categorias.objects.create(
            id = categoria.get("id"),
            nome = categoria.get("nome"),
            palavras_chave = categoria.get("palavras_chave"),
            descrição = categoria.get("descrição"),
            imagem = # Load File 
            categoria_pai = categoria.get("categoria_pai")
        )

# ENDEREÇO
with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile1:
    with open("{}/{}".format(OLD_DATABASE, TABLES.get("cidades")), "r", encoding="utf-8") as inputfile2:
        with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimento_cidades")), "r", encoding="utf-8") as inputfile3:
            for endereco in JSONParser.endereco(file = inputfile1, file_cidades = inputfile2, cidades_estabelecimentos = inputfile3):
                models.Endereco.objects.create(
                    cidade = models.Cidade.objects.get(id = endereco.get("cod_cidade")),
                    bairro = endereco.get("bairro"),
                    logradouro = endereco.get("logradouro"),
                    numero = endereco.get("numero")
                )

# DADOS DIVULGAÇÃO
with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile:
    for estabelecimento in JSONParser.dados_divulgacao(inputfile):
        models.DadosDivulgacao.objects.create(
            nome = estabelecimento.get("nome"),
            descricao = estabelecimento.get("descricao"),
            site = estabelecimento.get("site")
        )

# IMAGENS ESTABELECIMENTO
with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile1:
    with open("{}/{}".format(OLD_DATABASE, TABLES.get("galeria")), "r", encoding="utf-8") as inputfile2:
        transfer = FTPTransfer.Transfer()
        for estabelecimento in JSONParser.imagens_estabelecimento(inputfile1, inputfile2):
            
            imagensestabelecimento = models.ImagensEstabelecimento(
                nome_estabelecimento = estabelecimento.get("nome_estabelecimento")
            )

            if estabelecimento.get("imagem_cartao"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_cartao"))

                imagensestabelecimento.imagem_cartao.save(
                    estabelecimento.get("imagem_cartao"),
                    File(open(estabelecimento.get("imagem_cartao"), "rb"))
                )

                transfer.remove_localfile(filename = estabelecimento.get("imagem_cartao"))

            if estabelecimento.get("imagem_1"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_1"))

                imagensestabelecimento.imagem_1.save(
                    estabelecimento.get("imagem_1"),
                    File(open(estabelecimento.get("imagem_1"), "rb"))
                )
                
                transfer.remove_localfile(filename = estabelecimento.get("imagem_1"))
            else:
                continue

            if estabelecimento.get("imagem_2"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_2"))

                imagensestabelecimento.imagem_2.save(
                    estabelecimento.get("imagem_2"),
                    File(open(estabelecimento.get("imagem_2"), "rb"))
                )
                
                transfer.remove_localfile(filename = estabelecimento.get("imagem_2"))
            else:
                continue

            if estabelecimento.get("imagem_3"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_3"))

                imagensestabelecimento.imagem_3.save(
                    estabelecimento.get("imagem_3"),
                    File(open(estabelecimento.get("imagem_3"), "rb"))
                )
                
                transfer.remove_localfile(filename = estabelecimento.get("imagem_3"))
            else:
                continue

            if estabelecimento.get("imagem_4"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_4"))

                imagensestabelecimento.imagem_4.save(
                    estabelecimento.get("imagem_4"),
                    File(open(estabelecimento.get("imagem_4"), "rb"))
                )

                transfer.remove_localfile(filename = estabelecimento.get("imagem_4"))
            else:
                continue

            if estabelecimento.get("imagem_cartao"):
                transfer.get_remotefile(filename = estabelecimento.get("imagem_cartao"))

                imagensestabelecimento.imagem_cartao.save(
                    estabelecimento.get("imagem_cartao"),
                    File(open(estabelecimento.get("imagem_cartao"), "rb"))
                )

                transfer.remove_localfile(filename = estabelecimento.get("imagem_cartao"))
            else:
                continue


# FATO ESTABELECIMENTO
def main():

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
        "galeria" : "guiacome_site_table_galeria.json"
    }

    with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimentos")), "r", encoding="utf-8") as inputfile:
        with open("{}/{}".format(OLD_DATABASE, TABLES.get("ciades")), "r", encoding="utf-8") as inputfile2:
            with open("{}/{}".format(OLD_DATABASE, TABLES.get("estabelecimento_cidades")), "r", encoding="utf-8") as inputfile3:
        
                enderecos = JSONParser.endereco(inputfile, inputfile2, inputfile3)

                for estabelecimento in JSONParser(inputfile, None, None, None, None, None):
                    fato = models.FatoEstabelecimento.objects.create(
                        id = estabelecimento.get("id"),
                        nome = estabelecimento.get("nome"),
                        CNPJ_estabelecimento = estabelecimento.get("CNPJ_estabelecimento"),
                        nome_responsavel = estabelecimento.get("nome_responsavel"),
                        telefone_contato_1 = estabelecimento.get("telefone_contato_1"),
                        telefone_contato_2 = estabelecimento.get("telefone_contato_2"),
                        email_contato = estabelecimento.get("email_contato"),
                        observacoes = estabelecimento.get("observacoes"),
                        descricao = estabelecimento.get("descricao"),
                        status_destaque = estabelecimento.get("status_destaque"),
                        impulsionamentos = estabelecimento.get("impulsionamentos"),
                        nota = estabelecimento.get("nota"),
                        categoria = estabelecimento.get("categoria"),
                        endereco_fiscal = estabelecimento.get("endereco_fiscal"),
                        endereco_comercial = estabelecimento.get("endereco_comercial"),
                        dados_divulgacao = estabelecimento.get("dados_divulgacao"),
                        imagens_divulgacao = estabelecimento.get("imagens_divulgacao")
                    )

                    for endereco in enderecos
                        if endereco.get("cod_estabelecimento") == fato.id:
                            addr = models.Endereco.objects.create(
                                cidade = endereco.get("cod_cidade"),
                                bairro = endereco.get("bairro"),
                                logradouro = endereco.get("endereco"),
                                numero = endereco.get("numero")
                            )

                            break
                    
                    fato.endereco_fiscal = addr
                    fato.endereco_comercial = addr
                    fato.save()

                    break
