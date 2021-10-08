# Trabalho Sistemas Web 2021

[Como colaborar com esse projeto](#como-colaborar-com-esse-projeto)

[Iniciar ambiente virtual](#iniciar-ambiente-virtual)

[Instalar dependências](#instalar-dependências)

[Ativar o modo desenvolvimento](#ativar-o-modo-desenvolvimento)

[Iniciar o server](#iniciar-o-server)

## Como colaborar com esse projeto

- [ ] Inicie seu ambiente virtual. Obs: Aqui estou usando Pipenv, mas pode utilizar venv sem problemas
- [ ] Instale as dependências. Para compatibilidade, manterei um Pipfile(usado pelo pipenv) e um arquivo de requeriments.txt
- [ ] Ative o modo desenvolvimento
- [ ] Inicie o server

## Iniciar ambiente virtual

Inicie seu ambiente virtual. Obs: Aqui estou usando Pipenv, mas pode utilizar venv sem problemas

``` shell
pipenv shell
```

## Instalar dependências

Instale as dependências. Para compatibilidade, manterei um Pipfile(usado pelo pipenv) e um arquivo de requeriments.txt

``` shell
pipenv install
```

## Ativar o modo desenvolvimento

``` shell
export FLASK_ENV=development
```

## Iniciar o server

``` shell
flask run
```
