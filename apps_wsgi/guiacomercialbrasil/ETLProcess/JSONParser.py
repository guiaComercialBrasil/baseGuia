import json

def fato_estabelecimento(file):
    data = json.load(file).get("data")
    cleaned_data = []
    for estabelecimento in data:
        cleaned_estabelecimento = {
            "id" : estabelecimento.get("cod_estabelecimento"),
            "nome" : estabelecimento.get("razao_social") if len(estabelecimento.get("razao_social")) > 0 else estabelecimento.get("nome"),
            # slug is auto generated
            "CNPJ_estabelecimento" : estabelecimento.get("cnpj"),
            "nome_responsavel" : estabelecimento.get("responsavel"),
            "CPF_responsavel" : estabelecimento.get("cpf_cnpj") if len(estabelecimento.get("cpf_cnpj")) < 14 else None,
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

        cleaned_data.append(cleaned_estabelecimento)

    return cleaned_data

def categoria(file):
    '''
    base file: guiacome_site_table_categoria.json
    '''
    data = json.load(file).get("data")
    cleaned_data = []
    for categoria in data:
        cleaned_categoria = {
            "id" : categoria.get("cod_categoria"),
            "nome" : categoria.get("categoria"),
            "palavras_chave" : categoria.get("keywords"),
            "descrição" : categoria.get("descritivos"),
            "imagem" : categoria.get("imagem") if len(categoria.get("imagem")) > 3 else None,
            "categoria_pai" : categoria.get("categoria_pai")
        }

        cleaned_data.append(cleaned_categoria)

    return cleaned_data

def dados_divulgacao(file):
    '''
    base file: guiacome_site_table_estabelecimento.json
    '''
    data = json.load(file).get("data")
    cleaned_data = []
    for d_divulgacao in data:
        cleaned_dados = {
            "cod_estabelecimento" : d_divulgacao.get("cod_estabelecimento"),
            "nome" : d_divulgacao.get("razao_social") if len(d_divulgacao.get("razao_social")) > 0 else d_divulgacao.get("nome"),
            "descricao" : d_divulgacao.get("descricao", "Importado do Banco de Dados Legado."),
            "telefone" : None,
            "whatsapp" : None,
            "site" : d_divulgacao.get("site"),
            "instagram" : None,
            "facebook" : None,
            "twitter" : None,
            "linkedin" : None
        }

        cleaned_data.append(cleaned_dados)

    return cleaned_data

def endereco(file, file_cidades, cidades_estabelecimentos):
    '''
    base file: 
        - guiacome_site_table_estabelecimento.json,
        - guiacome_site_table_cidade.json,
        - guiacome_site_table_estabelecimento_cidades.json
    '''

    data = json.load(file).get("data")

    cidades = json.load(file_cidades).get("data")
    cidades_estabelecimentos = json.load(cidades_estabelecimentos).get("data")

    cleaned_data = []
    for endereco in data:

        for cidade_estabelecimento in cidades_estabelecimentos:
            if cidade_estabelecimento.get("cod_estabelecimento") == endereco.get("cod_estabelecimento"):
                cod_cidade = cidade_estabelecimento.get("cod_cidade")
                break
        for cidade in cidades:
            if cidade.get("cod_cidade") == cod_cidade:
                nome_cidade = cidade.get("cidade") 
                estado = cidade.get("uf")

        cleaned_endereco = {
            "cod_estabelecimento" : endereco.get("cod_estabelecimento"),
            "nome_cidade" : nome_cidade, ## exportando id da cidade DEVE SER TRATADO NO DJANGO
            "bairro" : endereco.get("bairro"),
            "logradouro" : endereco.get("endereco"),
            "numero" : endereco.get("numero"),
            "estado" : estado
        }

        cleaned_data.append(cleaned_endereco)

    return cleaned_data    

def cidade(file):
    '''
    base file: guiacome_site_table_cidade.json
    '''
    data = json.load(file).get("data")

    cleaned_data = []

    for cidade in data:
        cleaned_cidade = {
            "id" : cidade.get("id"),
            "pais" : "BR",
            "estado" : cidade.get("uf"),
            "cidade" : cidade.get("cidade")
        }

        cleaned_data.append(cleaned_cidade)

    return cleaned_data

def imagens_estabelecimento(file, galeria):
    '''
    base file: guiacome_site_table_estabelecimento.json + guiacome_site_table_galeria.json
    '''
    data = json.load(file).get("data")
    galeria = json.load(galeria).get("data")


    cleaned_data = []

    for estabelecimento in data:
        
        cod_estabelecimento = estabelecimento.get("cod_estabelecimento")

        imagens = []
        for imagem in galeria:
            if len(imagens) == 5:
                break
            if imagem.get("cod_estabelecimento") == cod_estabelecimento:
                imagens.append(imagem.get("imagem"))


        cleaned_imagens = {
            "cod_estabelecimento" : cod_estabelecimento,
            "nome_estabelecimento" : estabelecimento.get("nome"),
            "imagem_cartao" : estabelecimento.get("imagem_cartao"),
            "imagem_1" : imagens[0] if len(imagens) >= 1 else None,
            "imagem_2" : imagens[1] if len(imagens) >= 2 else None,
            "imagem_3" : imagens[2] if len(imagens) >= 3 else None,
            "imagem_4" : imagens[3] if len(imagens) >= 4 else None,
            "imagem_5" : imagens[4] if len(imagens) == 5 else None
        }

        cleaned_data.append(cleaned_imagens)

    return cleaned_data