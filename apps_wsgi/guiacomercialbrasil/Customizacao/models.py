from django.db import models

# Create your models here.
class Customizacao(models.Model):

    class Meta():
        verbose_name = "Customização"
        verbose_name_plural = "Customizações"

    pagina = models.CharField(max_length = 200, unique = True)
    texto_1 = models.TextField(null = True, blank = True)
    texto_2 = models.TextField(null = True, blank = True)

    def __str__(self):
        return self.pagina