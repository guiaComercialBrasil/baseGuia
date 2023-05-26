from Estabelecimentos import models

if __name__ == '__main__':
    dicla = models.FatoEstabelecimento.objects.get(id = 14)
    print(dicla)