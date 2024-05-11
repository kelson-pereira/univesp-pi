from django.conf import settings
from django.core import serializers
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from .models import Registro
from .forms import Localizar, Registrar
import googlemaps

google_api_key = settings.GOOGLE_API_KEY
google_map_id = settings.GOOGLE_MAP_ID

# Exibe a página com o formulário de registro
def principal(request):
    localizar = Localizar()
    registrar = Registrar()
    if request.method == "POST":
        localizar = Localizar(request.POST)
        if localizar.is_valid():
            try:
                gmaps = googlemaps.Client(key=google_api_key)
                cep = localizar.cleaned_data['cep']
                resultado = gmaps.geocode(f"{cep}, Brasil")
                componentes = resultado[0]['address_components']
                for componente in componentes:
                    if 'route' in componente['types']:
                        logradouro = componente['long_name']
                    elif 'sublocality' in componente['types']:
                        bairro = componente['long_name']
                    elif 'administrative_area_level_2' in componente['types']:
                        cidade = componente['long_name']
                    elif 'administrative_area_level_1' in componente['types']:
                        estado = componente['short_name']
                registrar.initial.setdefault('cep', localizar.cleaned_data['cep'])
                messages.success(request, f"{logradouro}, {bairro} - {cidade}/{estado}", extra_tags='success')
            except:
                localizar.add_error('cep', 'Favor informar um CEP válido. Ex: 12345-678')
                messages.error(request, 'CEP inválido.', extra_tags='error')
        else:
            messages.error(request, 'CEP inválido.', extra_tags='error')
    return render(request, "app/principal.html", {"localizar": localizar, "registrar": registrar})

# Salva o registro no banco de dados.
def registrar(request):
    localizar = Localizar()
    registrar = Registrar()
    if request.method == "POST":
        localizar = Localizar(request.POST)
        registrar = Registrar(request.POST)
        if registrar.is_valid():
            cep = registrar.cleaned_data['cep']
            gmaps = googlemaps.Client(key=google_api_key)
            resultado = gmaps.geocode(f"{cep}, Brasil")
            componentes = resultado[0]['address_components']
            for componente in componentes:
                if 'postal_code' in componente['types']:
                    cep = componente['long_name']
                elif 'route' in componente['types']:
                    logradouro = componente['long_name']
                elif 'sublocality' in componente['types']:
                    bairro = componente['long_name']
                elif 'administrative_area_level_2' in componente['types']:
                    cidade = componente['long_name']
                elif 'administrative_area_level_1' in componente['types']:
                    estado = componente['short_name']
            numero = registrar.cleaned_data['numero']
            localizacao = gmaps.geocode(f"{logradouro}, {numero}, {cidade}, {estado}, Brasil")
            registro = Registro()
            registro.descricao = registrar.cleaned_data['descricao']
            registro.nome = registrar.cleaned_data['nome']
            registro.telefone = registrar.cleaned_data['telefone']
            registro.cep = cep
            registro.endereco = logradouro
            registro.numero = registrar.cleaned_data['numero']
            registro.bairro = bairro
            registro.cidade = cidade
            registro.estado = estado
            registro.latitude = localizacao[0]['geometry']['location']['lat']
            registro.longitude = localizacao[0]['geometry']['location']['lng']
            registro.termos = registrar.cleaned_data['termos']
            registro.save()
            return HttpResponseRedirect(reverse('registros'))
    return render(request, "app/principal.html", {"localizar": localizar, "registrar": registrar})

# Lista os registros do banco de dados
def registros(request):
    forty_days = timezone.now() - timedelta(days = 40)
    registros = {'registros': Registro.objects.filter(datahora__gte=forty_days).values('ident', 'datahora', 'cep', 'numero', 'descricao')}
    return render(request, 'app/registros.html', registros)

# Apaga o registro no banco de dados.
def apagar(request):
    if request.method == "POST":
        ident = request.POST.get('ident')
        telefone = request.POST.get('telefone')
        try:
            registro = Registro.objects.get(ident=ident, telefone=telefone)
            registro.delete()
            messages.success(request, 'O registro foi apagado com sucesso.', extra_tags='text-bg-success')
        except:
            messages.error(request, 'O registro não pôde ser apagado.', extra_tags='text-bg-danger')
    return HttpResponseRedirect(reverse('registros'))

# Exibe no mapa os registros do banco de dados
def mapa(request):
    forty_days = timezone.now() - timedelta(days = 40)
    registros = serializers.serialize("json", Registro.objects.filter(datahora__gte=forty_days), fields=["latitude", "longitude"])
    return render(request, 'app/mapa.html', {"registros": registros, "google_api_key": google_api_key, "google_map_id": google_map_id})

# Exibe a política de privacidade
def politica(request):
    return render(request, "app/politica.html")