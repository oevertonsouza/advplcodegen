# advplcodegen
Framework de geração de códigos ADVPL orientado a objetos.

# Sobre o projeto
O propósito desse projeto é utilizar classes abstratas que possuam métodos que abrangem o máximo de funções necessárias prédispostas para qualquer projeto ADVPL, tais como, CRUD, paginação de busca, ordenação de resultados, retorno de colunas especificas de um resultado para API's, mapper de objeto para Json e geração de endpoints.

# Compatibilidade / Ambientes homologados

* Python 3x 
* 1 Sqlserver 2012 
* 2 Protheus 12.1.17

# Pré-requisitos

Python 3 instalado, base de dados e ambiente de desenvolvimento (ADVPL) protheus configurados.

# Configuração de Ambiente

* 1 - Faça o clone do projeto.
* 2 - No arquivo settings.py preencha os dados de acesso ao banco de dados do seu ambiente Protheus.

NAME = Nome do banco de dados do seu ambiente.</br>
USER = Usuário do bando de dados</br>
PASSWORD = Senha do seu banco de dados</br>
HOST = Hostname ou IP do seu banco de dados.</br>

Exemplo.

```python

DATABASES = {
    'default': {
        'NAME': 'ProtheusDb',
        'USER': 'sa',
        'PASSWORD': 'admin123',
        'HOST': 'localhost',
    }
}

```
* 3 - Ainda no arquivo settings.py preencha os dados do seu ambiente Protheus.

EMPRESA = Empresa prefixo das tabelas no seu dicionário</br>
FILIAL = Filial do seu ambiente</br>
SEGMENT = Seguimento em que atua.</br>
PREFIX = Prefixo com 3 caracteres, será o prefixo das suas classe e nome de fontes para distinguir dos fontes já existentes.</br>

-Especificos para gerção de APIS e documentação no padrão OpenAapi em Json.
SEGMENT = Seguimento qual o produto esta alocado.
PRODUCT = Nome do produto.
PRDUCT_DESCRIPTION = Descrição do produto.
CONTACT = Email de Contato do produto.

Exemplo:

```python
PROTHEUS_ENVIORMENT = {
    'default': {
        'EMPRESA' : 'T1',
        'FILIAL' : 'M SP 01',
        'PREFIX' : 'Cen',
        'SEGMENT' : 'HealthCare',        
        'PRODUCT' : 'Central de Obrigações',
        'PRDUCT_DESCRIPTION' : 'Central de Obrigações, para controle de legislações de operadoras de convênio de saúde.',
        'CONTACT' : 'centraldeobrigacoes@totvs.com.br',
    }
}
```

# Comandos

Para execução dos comandos acesse a arvore do projeto onde se encontra o fonte advplcodegen.py, todos os comandos partirão desse fonte.</br>
<b>Comano testconnect</b></br>
Para testar a conexão com o banco.
</br>

```console
$ advplcodegen.py testconnect
```

<b>Comando startproject</b><br>
Para iniciar um projeto.
</br>

```console
$ advplcodegen.py startproject
```

Nota:<br>
Após a execução desse comando os diretório do projeto assim como suas libs deverão serem criadas em SRC, algo como o exemplo abaixo.
</br>
</br>

![SRC arvore do projeto](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/src.png)

<b>Comando addentity</b><br>
Para adicionar uma entidade ao projeto, passando o nome da entidade e sua descrição em ingles no singular.
</br>

```console
$ advplcodegen.py addentity <entidade> <nome da entidade em inglês> <nome da coluna chave da tabela>
```

Exemplo:

```console
$ advplcodegen.py addentity B3JT10 Product B3K_CODIGO
```

Nota:<br>
No exemplo acima o parametro passado B3K_CODIGO, será a coluna usada no Parametro do Path da sua API, nos verbos de get e delete, os demais dados do indice primario da tabela, serão usado como Parametros da query, para os mesmos verbos.<br>
Neste mesmo exemplo usamos a tabela B3JT10, o indice primario dessa tabela é composta pelas colunas B3K_CODIGO e B3K_CODOPE,<br>
portanto uma requisição get de um unico registro funcionará da seguinte maneira.<br>
<br>
http://localhost/api/healthcare/v1/product/[b3kcodigo]?b3kcodiope=[b3kcodiope]<br>
<br>
Exemplo com o preenchimento dos dados.<br>
<br>
http://localhost/api/healthcare/v1/product/5561003?b3kcodiope=417505<br>
<br>
Repare que healthcare na URL foi preenchido de acordo com o Segumento preenchido no arquivo settings.py, assim como "/product", que foi passado como parametro no comando addentity.<br>
<br>
Após a execução desse comando os arquivos de storage deverão serem criados, esses arquivos contem os dados necessários para criação dos fontes e documentações. Os arquivos terão um aspecto semelhante aos exemplos abaixo.
</br>

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/filestorage.png)





