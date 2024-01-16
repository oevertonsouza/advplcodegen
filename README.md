# advplcodegen
Framework de geração de códigos ADVPL orientado a objetos para API's.

# Sobre o projeto
O propósito desse projeto é utilizar classes abstratas que possuam métodos que abrangem o máximo de funções necessárias prédispostas para qualquer projeto ADVPL, tais como, CRUD, paginação de busca, ordenação de resultados, retorno de colunas especificas de um resultado para API's dos verbos GET, PUT, POST e DELETE, mapper de objeto para Json e geração de endpoints.

# Compatibilidade / Ambientes homologados

* Python 3x 
* 1 Sqlserver 2012 
* 2 Protheus ^12.1.17

# Pré-requisitos

* Python 3 instalado (https://www.python.org/downloads/)
* Pip instalado - Execute o arquivo get-pip.py
* Biblioteca PyMsSql instalada - pip install pymssql
* Biblioteca PeeWee instalada - pip install peewee
* Base de dados e ambiente de desenvolvimento (ADVPL) protheus configurados "Melhor uso com o dicionario Protheus no banco de dados".

# Configuração de Ambiente

* 1 - Faça o clone do projeto.
* 2 - No arquivo settings.py preencha os dados de acesso ao banco de dados do seu ambiente Protheus.

>NAME = Nome do banco de dados do seu ambiente.</br>
USER = Usuário do bando de dados</br>
PASSWORD = Senha do seu banco de dados</br>
HOST = Hostname ou IP do seu banco de dados.</br>

Exemplo:

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

>EMPRESA = Empresa prefixo das tabelas no seu dicionário</br>
FILIAL = Filial do seu ambiente</br>
SEGMENT = Seguimento em que atua.</br>
PREFIX = Prefixo com 3 caracteres, será o prefixo das suas classe e nome de fontes para distinguir dos fontes já existentes.</br>
DICTIONARY_IN_DATABASE = Indica se o ambiente Protheus possui dicionário de dados no banco ou não</br>

-Especificos para geração de APIS e documentação no padrão OpenApi em Json.</br>
>SEGMENT = Seguimento qual o produto esta alocado.</br>
PRODUCT = Nome do produto.</br>
PRDUCT_DESCRIPTION = Descrição do produto.</br>
CONTACT = Email de Contato do produto.</br>

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
        'DICTIONARY_IN_DATABASE' : True,
    }
}
```

# Comandos e criação do projeto ADVPL.

Para execução dos comandos acesse a arvore do projeto onde se encontra o fonte advplcodegen.py, todos os comandos partirão desse fonte.</br></br>
<b>Comando testconnect</b>  
Para testar a conexão com o banco.  


```console
$ advplcodegen.py testconnect
```

## Comando startproject
Inicia um projeto e cria a estrutura de pastas e arquivos.  


```console
$ advplcodegen.py startproject
```

**Nota:** 
Após a execução desse comando os diretório do projeto assim como suas libs deverão ser criadas em SRC, algo como o exemplo abaixo.  

![SRC arvore do projeto](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/master/docImg/src.png)

## Comando addentity
Adiciona uma entidade ao projeto.  
Esse processo irá alimentar a tabela "entity" que armazena os principais dados da entidade.  
Para cada entidade adicionada irá alimentar a tabela "colunas" que armazena os dados das colunas da entidade.  
Essas tabelas podem ser acessadas e customizadas por meio do comando "openDb" detalhado mais abaixo.  
O conteúdo dessas tabelas é lido pelo gerador de código e determina o nome dos arquivos, variáveis e tags dos JSONs das APIs.  

<b>Parametros:</b>  
><b>Entidade:</b> Nome da entidade qual os fontes e API, serão destinados.  
<b>Coluna chave:</b> Deverá ser referenciado uma e apenas uma coluna como chave, essa coluna será usada como parametro do Path da sua API.  
<b>Nome abreviado:</b> Nome com 4 caracteres que será utilizado para nomear as classes e arquivos referentes a essa entidade.  
<b>Nome da entidade em Ingles:</b> Nome da tabela no banco de dados em Ingles, deve ser em ingles devido ao comite de API.  
<b>Nome da entidade em português:</b> Nome da tabela no banco de dados em português.  

**Nota:** Caso o ambiente possua dicionário no banco de dados, os parâmetros "nome da entidade em inglês" e "nome da entidade em português" serão opcionais.  
Nessa situação as colunas das entidades também terão os nomes retirados automaticamente do dicionário de dados.<br>

```console
$ advplcodegen.py addentity <entidade> <coluna chave> <nome abreviado> [<nome da entidade em inglês> <nome da entidade em português>]
```

Exemplo:

```console
$ advplcodegen.py addentity B3JT10 B3J_CODIGO Prod Product Produto
```

**Nota:** No exemplo acima o parametro passado B3J_CODIGO, será a coluna usada no Parametro do Path da sua API, nos verbos de get, put e delete, os demais dados do indice primario da tabela serão usados como Parametros da query, para os mesmos verbos.<br>
Neste mesmo exemplo usamos a tabela B3JT10, o indice primario dessa tabela é composta pelas colunas B3J_CODIGO e B3J_CODOPE,<br>
portanto uma requisição get de um unico registro funcionará da seguinte maneira.  
  
```
http://localhost/api/healthcare/v1/product/[b3jcodigo]?b3jcodope=[b3Jcodope]  
```
Exemplo com o preenchimento dos dados.
```
http://localhost/api/healthcare/v1/product/5561003?b3Jcodope=123456<br>
```
Repare que healthcare na URL foi preenchido de acordo com o Seguimento preenchido no arquivo settings.py, assim como "/product", que foi passado como parametro no comando addentity.

## Comando addentities
Adiciona uma ou mais entidades a partir de um arquivo texto.  
A estrutura do arquivo deve ser "nome_da_tabela;campo_chave;nome_abreviado"  
Exemplo:
```
B3A;B3A_CODIGO;Obri
B3D;B3D_CODIGO;Comp
```


<b>Parametros:</b>  
><b>Caminho do arquivo:</b> Caminho relativo do arquivo a ser importado.  

```console
$ advplcodegen.py addentities <caminhdo do arquivo>
```

Exemplo:

```console
$ advplcodegen.py addentities entities.txt
```

## Comando openDb
Permite abrir o gerenciador do banco de dados interno do advplcodegen.  
O projeto possui um banco de dados SQLITE para registrar as entidades, relacionamentos, etc.  
Este banco é criado automaticamente ao executar o comando "startProject" dentro da pasta **\sqliteadmin**.  

```console
$ advplcodegen.py openDb
```

## Comando addRelation
Para adicionar um Relacionamento entre entidades ao projeto.  
Esse processo irá alimentar as tabelas de relacionamentos do projeto (Relations e RelationKeys).  

<b>Parametros:</b>  
><b>Tabela pai:</b> Nome da tabela pai do relacionamento.  
<b>Tabela filha:</b> Nome da tabela pai do relacionamento.  
<b>Comportamento:</b> Informar o tipo de comportamento do relacionamento quando um registro for deletado. Valores aceitáveis: 0 - Realiza a deleção somente na tabela pai; 1 - Realiza a deleção em modo de cascata deletando também as tabelas filhas.  
<b>Tipo de relacionamento:</b> Indica a cardinalidade do relacionamento. Valores aceitáveis: 1 - Relação N para N;2 - Relação 1 para N;3 - Relação N para 1;4 - Relação 0 para 1 ou N;5 - Relação N ou 1 para 0  
<b>Chaves do relacionamento:</b> Indica os campos que compões o relacionamento separados por virgula (,) podendo ou não ter concatenação de campos no formato: <tabela_pai_campo1>=<tabela_filha_campo1>,<tabela_pai_campo2>=<tabela_filha_campo2>+<tabela_filha_campo3>,...,<tabela_pai_campoN>=<tabela_filha_campoN>  

```console
$ advplcodegen.py addRelation <tabela pai> <tabela filha> <comportamento> <cardinalidade> <chaves>
```

Exemplo:

```console
$ advplcodegen.py addRelation B3K B3J 1 1 B3K_FILIAL=B3J_FILIAL,B3K_CODPRO=B3J_CODIGO
```

## Comando build
Comando para gerar os fontes para sua API's.  

```console
$ advplcodegen.py build
```
Após a execução desse comando será criando na arvore do seu projeto os fontes necessários para a sua API com os seguintes verbos, GET, POST, PUT e DELETE. conforme o exemplo abaixo.  

![Arquivos Gerados](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/master/docImg/fontesgerados.png)

É possível encontrar os exemplos de fontes gerados na pasta <b>/src_samples</b> do projeto padrão.  
Compile seus fontes e teste sua API usando Postman ou qualquer outro software de requisições HTTP rest.  

**Nota:** No metodo GET poderá ser executado como uma busca unica passando o valor da coluna chave escolhida no comando addentity no Parametro do Path, e as demais colunas do indice primario passados nos parametros query.  
Todos os funcionamentos requeridos no comite de API's estarão disponíveis, como retornar somente os campos solicitados, ordenar a busca, paginação do resultado de coleção e tratamento de erro.  

Caso tenha alguma duvida sobre a estrutura gerada haverá uma documentação da API em dois arquivos para cada API gerada, no diretório DOC do seu projeto no padrão OpenAPI, um arquivo com a strutura body e um arquivo com a estrutura da API, conforme o comite de API's.  
Caso a sua API não esteja funcionando ou com comportamento inadequado, haverá 5 casos de teste do CRUD do seu projeto em ADVPR no diretorio test do seu projeto.  

## Comando PO-START
Inicia um novo projeto Portinari (PO-UI) que consome as APIs geradas
Os passos da inicalização do projeto são:
* Instalar o angular
* Criar um novo projeto portinari chamado my-po-project
* Instalar o Portinari
* Instalar as dependências necessárias


```console
$ advplcodegen.py po-start
```

## Comando PO-BUILD
Cria os arquivos da aplicação angular baseado nas entidades adicionadas  

```console
$ advplcodegen.py po-build
```
## Comando PO-SERVE
Inicia o servidor e abre a aplicação no browser padrão (equivale ao comando ng serve -o)  

```console
$ advplcodegen.py po-serve
```

Colabore com esse projeto, caso tenha algum problema no uso ou sugestão, #issue.  

