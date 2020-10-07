from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput
from django import forms
from django.contrib.auth.models import User

from . import models


class MapaForm(forms.ModelForm):

    class Meta:
        model = models.Mapa
        fields = '__all__'
        
class MapaCamposForm(forms.ModelForm):
    
    class Meta:
        model = models.MapaCampos
        fields = '__all__'

class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label='Senha')
    class Meta:
        model = User
        fields = ['username','password']



class ApontamentoForm(forms.ModelForm):
    #data_apontamento = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y') )
    #hora_inicial = forms.TimeField(widget=TimePickerInput())
    #hora_final = forms.TimeField(widget=TimePickerInput())
    # tweak pra tranformar o input text para text area foi comentado
    # porque a informação editada grava, mas ao recarregar a pagina
    # a informação não volta.
    # atividade = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.Apontamento
        fields = ['periodo','projeto','recurso','data_apontamento','hora_inicial','hora_final','descricao']
        widgets = {
            'data_apontamento':DatePickerInput(format='%d/%m/%Y'),
            'hora_inicial':TimePickerInput(),
            'hora_final': TimePickerInput(),
        }
