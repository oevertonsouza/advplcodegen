# advplcodegen
Framework de geração de códigos ADVPL orientado a objetos.

# Sobre o projeto
O propósito desse projeto é utilizar classes abstratas que possuam métodos que abrangem o máximo de funções necessárias prédispostas para qualquer projeto ADVPL, tais como, CRUD, paginação de busca, ordenação de resultados, retorno de colunas especificas de um resultado para API's, mapper de objeto para Json e geração de endpoints.

# Compatibilidade

* Python 3x 
* 1 Sqlserver 2012 
* 2 Protheus 12.1.17

# Pré-requisitos

Python 3 instalado, base de dados e ambiente protheus configurados.

# Configuração de Ambiente

* 1 - Faça o clone do projeto.
* 2 - No arquivo settings.py preencha os dados de acesso ao banco de dados do seu ambiente Protheus.

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
* 3 - Ainda no arquivo settings.py preencha os dados do seu ambiente Protheus.

EMPRESA = Empresa prefixo das tabelas no seu dicionário
FILIAL = Filial do seu ambiente
SEGMENT = Seguimento em que vc atua
PREFIX = Prefixo com 3 caracteres, será o prefixo das suas classe e nome de fontes para distinguir dos fontes já existentes.

Exemplo:

```python
PROTHEUS_ENVIORMENT = {
    'default': {
        'EMPRESA': 'T1',
        'FILIAL': 'M SP 01',
        'SEGMENT' : 'HealthCare',
        'PREFIX' : 'Cen',
    }
}
```

-- Em construção
