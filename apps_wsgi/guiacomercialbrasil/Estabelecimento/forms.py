from django import forms

STATE_CHOICES = (
    ('', 'Selecione um Estado'),
	('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
	('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
	('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
	('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
	('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
	('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
	('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
	('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
	('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
	('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
)

class CityForm(forms.Form):
    estado = forms.ChoiceField(choices = STATE_CHOICES, required = True, label = "Selecione um Estado")
    cidade = forms.CharField(max_length = 200, required = True, label = "Digite uma Cidade", widget= forms.TextInput(attrs = {"placeholder" : "Digite uma Cidade"}))


class ContactMail(forms.Form):
    nome = forms.CharField(max_length = 200, required = True)
    email = forms.EmailField(required = True)
    assunto = forms.CharField(max_length = 300, required = True)
    mensagem = forms.CharField(required = True, widget = forms.Textarea)
