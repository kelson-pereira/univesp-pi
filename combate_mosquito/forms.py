from django import forms
from django.core.validators import RegexValidator

class Localizar(forms.Form):
    error_css_class = "is-invalid"
    cep = forms.CharField(label='Informe o CEP do local do foco*', widget=forms.TextInput(attrs={'class':'form-control'}), validators=[RegexValidator('([0-9]{8}|[0-9]{5}-[0-9]{3})', message='Favor informar um CEP válido. Ex: 12345678 ou 12345-678')])

class Registrar(forms.Form):
    error_css_class = "is-invalid"
    cep = forms.CharField(label='', widget=forms.HiddenInput(), validators=[RegexValidator('^([0-9]{8}|[0-9]{5}-[0-9]{3})+$')])
    numero = forms.CharField(label='Informe o número do local do foco*', widget=forms.TextInput(attrs={'class':'form-control'}), validators=[RegexValidator('^[0-9]*$', message='Favor informar um número válido. Ex: 123')])
    descricao = forms.CharField(label='Descreva o local suspeito. Ex: latas, garrafas, pneus, etc. (opcional)', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    telefone = forms.CharField(label='Informe seu telefone*', widget=forms.TextInput(attrs={'class':'form-control'}), validators=[RegexValidator('^([0-9]{11})$', message='Favor informar um telefone válido com DDD (somente números). Ex: 12987654321')])
    nome = forms.CharField(label='Informe seu nome (opcional)', required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    termos = forms.BooleanField(label='Concordo com a política de privacidade.', widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))