# advplcodegen
Framework de geração de códigos ADVPL orientado a objetos.

# Sobre o projeto
O propósito desse projeto é utilizar classes abstratas que possuam métodos que abrangem o máximo de funções necessárias prédispostas para qualquer projeto ADVPL, tais como, CRUD, paginação de busca, ordenação de resultados, retorno de colunas especificas de um resultado para API's, mapper de objeto para Json e geração de endpoints.

# Compatibilidade

Sqlserver 2012
Protheus 12.1.17

# Pré-requisitos

Base de dados e ambiente protheus configurados.

# Configuração de Ambiente

* Item 1 - Faça o clone do projeto.
* Item 2 - No arquivo settings.py preencha os dados de acesso ao banco de dados do seu ambiente.

```python

DATABASES = {
    'default': {
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'HOST',
    }
}

```
-- Em construção
