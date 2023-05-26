from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
import json, os, googlemaps, statistics


# Upload Paths
def upload_path_categoria(instance, filename):
    path = os.path.join("Categorias", "{}.{}".format(slugify(instance.nome), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_cartao(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "{}_cartao.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_1(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "1-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_2(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "2-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_3(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "3-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_4(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "4-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path

def upload_path_imagem_5(instance, filename):
    path = os.path.join(slugify(instance.nome_estabelecimento), "5-{}.{}".format(slugify(instance.nome_estabelecimento), filename[-3:]))
    if len(path) >= 250:
        path = path[:246] + path[-4:]
    return path


# Models
# Pre-Populated Models
class Cidade(models.Model):
    pais = models.CharField(max_length = 2)
    estado = models.CharField(max_length = 2)
    cidade = models.CharField(max_length = 200)

    latitude = models.CharField(max_length = 9, blank = True, null = True)
    longitude = models.CharField(max_length = 9, blank = True, null = True)


    def save(self, *args, **kwargs):
        if not (self.latitude and self.longitude):
            try:
                gmaps = googlemaps.Client(key = settings.GMAPS_KEY)
                geocode_string = gmaps.geocode("{}/{} - {}".format(
                    self.cidade, self.estado, self.pais
                    ))
                coordinates = geocode_string[0].get('geometry').get('location')

                self.latitude, self.longitude = str(coordinates.get('lat'))[:9], str(coordinates.get('lng'))[:9]

            except:
                self.latitude, self.longitude = None, None
        super(Cidade, self).save(*args, **kwargs)

    def __str__(self):
        return "{}/{} - {}".format(self.cidade, self.estado, self.pais)


# User Populated Models
class Categoria(models.Model):
    # Regular Properties
    nome            = models.CharField(max_length = 200, unique = True)
    palavras_chave  = models.TextField(max_length = 1000, null = True, blank = True)
    descrição       = models.TextField(max_length = 1000)

    imagem          = models.ImageField(upload_to = upload_path_categoria, null = True, blank = True)

    slug = models.SlugField(blank = True)

    # Foreign Relation to Self (Recursive Construct)
    categoria_pai = models.ForeignKey('self', models.CASCADE, related_name = 'subcategoria', null = True, blank = True)

    # Control Systemic Properties
    data_cadastro = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)

    def subcategorias_validas(self):
        return self.subcategoria.filter(estabelecimentos_categorias__ativo = True).distinct()


    def get_palavras_chave(self, *args, **kwargs):
        return self.palavras_chave.replace(" ", "").split(",")

    def __str__(self):
#        if self.categoria_pai:
#            return "{} - {}".format(self.categoria_pai, self.nome)
#        else:
        return "{}".format(self.nome)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super(Categoria, self).save(*args, **kwargs)

class Endereco(models.Model):
    # Regular Properties
    cidade = models.ForeignKey(Cidade, models.CASCADE, 'endereco_cidade')
    bairro = models.CharField(max_length = 200, null = True, blank = True)
    logradouro = models.CharField(max_length = 200, null = True, blank = True)
    numero = models.CharField(max_length = 30 , null = True, blank = True)

    latitude = models.CharField(max_length = 9, blank = True, null = True)
    longitude = models.CharField(max_length = 9, blank = True, null = True)

    def save(self, *args, **kwargs):
        if not (self.latitude and self.longitude):
            try:
                gmaps = googlemaps.Client(key = settings.GMAPS_KEY)
                geocode_string = gmaps.geocode("{}, {} - {} - {}/{} - {}".format(
                    self.logradouro, self.numero, self.bairro, self.cidade.cidade, self.cidade.estado, self.cidade.pais
                    ))
                coordinates = geocode_string[0].get('geometry').get('location')
                self.latitude, self.longitude = str(coordinates['lat'])[:9], str(coordinates['lng'])[:9]
            except:
                pass
        super(Endereco, self).save(*args, **kwargs)

    def __str__(self, *args, **kwargs):

        if self.logradouro:    
            return "{}, {} - {} - {}".format(
                    self.logradouro, self.numero, self.bairro, self.cidade
                    )
        else:
            return str(self.cidade)

class DadosDivulgacao(models.Model):

    class Meta():
        verbose_name = "Dados Divulgação"
        verbose_name_plural = "Dados Divulgações"

    nome = models.CharField(max_length = 200)
    descricao = models.CharField(max_length = 3000)
    telefone = models.CharField(max_length = 13, blank = True, null = True)
    whatsapp = models.CharField(max_length = 13, blank = True, null = True)
    site = models.URLField(blank = True, null = True)

    # Social Media
    instagram = models.URLField(blank = True, null = True)
    facebook = models.URLField(blank = True, null = True)
    twitter = models.URLField(blank = True, null = True)
    linkedin = models.URLField(blank = True, null = True)

    def save(self, *args, **kwargs):
        if not self.nome:
            self.nome = self.estabelecimento_dados_divulgacao.nome
        super(DadosDivulgacao, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome

class ImagensEstabelecimento(models.Model):

    class Meta():
        verbose_name = "Imagens Estabelecimento"
        verbose_name_plural = "Imagens Estabelecimentos"

    nome_estabelecimento = models.CharField(max_length = 200, unique = True)
    imagem_cartao = models.ImageField(upload_to = upload_path_cartao)
    imagem_1 = models.ImageField(upload_to = upload_path_imagem_1, null = True, blank = True)
    imagem_2 = models.ImageField(upload_to = upload_path_imagem_2, null = True, blank = True)
    imagem_3 = models.ImageField(upload_to = upload_path_imagem_3, null = True, blank = True)
    imagem_4 = models.ImageField(upload_to = upload_path_imagem_4, null = True, blank = True)
    imagem_5 = models.ImageField(upload_to = upload_path_imagem_5, null = True, blank = True)

    def __str__(self):
        return self.nome_estabelecimento

class FatoEstabelecimento(models.Model):

    class Meta():
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"


    # Active Property
    ativo = models.BooleanField(default = True)

    # Regular Properties
    nome = models.CharField(max_length = 200, unique = True)
    slug = models.SlugField(blank = True, max_length = 255)
    CNPJ_estabelecimento = models.CharField(max_length = 18, null = True, blank = True)

    nome_responsavel = models.CharField(max_length = 200, null = True, blank = True)
    CPF_responsavel = models.CharField(max_length = 14, null = True, blank = True)

    telefone_contato_1 = models.CharField(max_length = 50, null = True, blank = True)
    telefone_contato_2 = models.CharField(max_length = 50, null = True, blank = True)

    email_contato = models.EmailField(null = True, blank = True)

    observacoes = models.TextField(null = True, blank = True)
    descricao = models.TextField(null = True, blank = True)

    keywords = models.TextField(null = True, blank = True)

    status_destaque = models.BooleanField(default = False)
    impulsionamento = models.IntegerField(default = 0)
    nota = models.DecimalField(max_digits = 3, decimal_places = 2, default = 3)

    # Foreign Relations
    categoria = models.ManyToManyField(Categoria, related_name = 'estabelecimentos_categorias', null = True, blank = True)
    endereco_fiscal = models.ForeignKey(Endereco, models.SET_NULL, related_name = 'estabelecimento_endereco_fiscal', blank = True, null = True)
    endereco_comercial = models.ForeignKey(Endereco, models.SET_NULL, related_name = 'estabelecimento_endereco_comercial', blank = True, null = True)
    dados_divulgacao = models.OneToOneField(DadosDivulgacao, models.SET_NULL, blank = True, null = True, related_name = 'estabelecimento_dados_divulgacao')
    imagens_divulgacao = models.OneToOneField(ImagensEstabelecimento, models.SET_NULL, blank = True, null = True)

    # Control Systemic Properties
    data_cadastro = models.DateField(auto_now_add = True)
    data_ultima_modificacao = models.DateField(auto_now = True)

    alcance_nacional = models.BooleanField(default = False)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.nota > 5:
            self.impulsionamento = Impulsionamento.objects.filter(estabelecimento = self).count()
        try:
            self.slug = slugify(self.nome)
        except:
            pass    

        super(FatoEstabelecimento, self).save(*args, **kwargs)

class Impulsionamento(models.Model):
    DURACAO =  60  * 60 * 3

    estabelecimento = models.ForeignKey(FatoEstabelecimento, models.CASCADE, "impulsionamento_estabelecimento")
    usuario = models.ForeignKey(User, models.CASCADE, "impulsionamento_usuario", blank = True, null = True)

    IP = models.GenericIPAddressField(blank = True, null = True)
    timestamp = models.DateTimeField(auto_now_add = True)
    data = models.DateField(auto_now_add = True)

    def __str__(self):
        if self.IP:
            return "{} | {} | {}".format(self.estabelecimento, self.IP, timezone.localtime(self.timestamp))
        else:
            return str(self.estabelecimento)

class Nota(models.Model):
    NOTA_RANGE = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    estabelecimento = models.ForeignKey(FatoEstabelecimento, models.CASCADE, "nota_estabelecimento")
    usuario = models.ForeignKey(User, models.CASCADE, "nota_usuario", blank = True, null = True)
    IP = models.GenericIPAddressField()
    nota = models.IntegerField(choices = NOTA_RANGE, default = 3)
    data = models.DateField(auto_now_add = True)


    def save(self, *args, **kwargs):
        if not self.nota > 5:
            super(Nota, self).save(*args, **kwargs)

    def __str__(self):
        return "{} - Nota {}".format(self.estabelecimento, self.nota)

    class Meta:
        unique_together = ["IP", "estabelecimento"]


# Signalized Functions
@receiver(post_save)
def summarize_impulsionamentos(sender, instance, **kwargs):
    if sender._meta.model_name == "impulsionamento":
        instance.estabelecimento.impulsionamento = Impulsionamento.objects.filter(estabelecimento = instance.estabelecimento).count()
        instance.estabelecimento.save()
    elif sender._meta.model_name == "nota":
        instance.estabelecimento.nota = instance.estabelecimento.nota_estabelecimento.all().aggregate(Avg('nota'))['nota__avg']
        instance.estabelecimento.save()


@receiver(post_delete)
def submission_delete(sender, instance, **kwargs):
    try:
        if sender._meta.model_name == 'Categoria':
            instance.imagem.delete(False)
        elif sender._meta.model_name == 'imagensestabelecimento':
            instance.imagem_cartao.delete(False)
            instance.imagem_1.delete(False)
            instance.imagem_2.delete(False)
            instance.imagem_3.delete(False)
            instance.imagem_4.delete(False)
            instance.imagem_5.delete(False)
        elif sender._meta.model_name == 'fatoestabelecimento':
            instance.imagens_divulgacao.delete(False)
    except:
        pass
