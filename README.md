# univesp-pi

## UNIVESP, 2024
### DRP03 Projeto Integrador em Computação I
### Grupo 018

### Comandos de instalação do django:

pip3 install django

### Comandos de inicialização do projeto:

django-admin startproject univesp_pi

mv univesp_pi univesp-pi && cd univesp-pi

django-admin startapp combate_mosquito

### Comandos para execução do projeto:

cd univesp-pi

python3 manage.py makemigrations

python3 manage.py migrate

python3 manage.py collectstatic --noinput --clear

python3 manage.py runserver 0.0.0.0:8000