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

Para execução dos comandos acesse a arvore do projeto onde se encontra o fonte advplcodegen.py, todos os comandos partirão desse fonte.</br></br>
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
Para adicionar uma entidade ao projeto.<br>
<b>Parametros:</b><br>
<b>Entidade:</b> Nome da entidade qual os fontes e API, serão destinados.<br>
<b>Nome da entidade em Ingles:<b> Nome da tabela no banco de dados em Ingles, deve ser em ingles devido ao comite de API.<br>
<b>Coluna chave:</b> Deverá ser referenciado uma e apenas uma coluna como chave, essa coluna será usada como parametro do Path da sua API.<br>
</br>

```console
$ advplcodegen.py addentity <entidade> <nome da entidade em inglês> <coluna chave>
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
Repare que healthcare na URL foi preenchido de acordo com o Seguimento preenchido no arquivo settings.py, assim como "/product", que foi passado como parametro no comando addentity.<br>
<br>
Após a execução desse comando os arquivos de storage deverão serem criados, esses arquivos contem os dados necessários para criação dos fontes e documentações.<br>
Os arquivos terão um aspecto semelhante aos exemplos abaixo, note que no arquivo .storage o nome do arquivo é é o nome da propria entidade.
</br>

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/filestorage.png)

Arquivo .entity</br>

Segue a seguinte estutura.</br>
|Nome da Entidade|Descrição em inglês da entidade|Coluna chave|<br>

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/entityfile.png)

Nota:<br>
Nesse exemplo temos duas tabelas adicionadas B3JT10 e B3KT10.<br>
<br>

Arquivo [entidade].storage</br>

Segue a seguinte estutura.</br>
|Nome da coluna|descrição da coluna|tipo da coluna|lenght da coluna|se a coluna faz parte do indice primario|coluna chave|

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/columnsfile.png)

Nota:<br>
Nesse arquivo você poderá alterar a segunda coluna para a descrição do campo da sua tabela em ingles conforme o comitê de API's, o como no exemplo abaixo.<br>
<br>

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/colunsfileinglishchange.png)

<br>
Caso isso não seja feito sua API tera o seguinte resultado.
<br>

![Arquivos Storage](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/apicampossemalterar.png)

</br>
<b>Comano build</b></br>
Comando para gerar os fontes para sua API's.
</br>

```console
$ advplcodegen.py build
```

<br>
Após a execução desse comando será criando na arvore do seu projeto os fontes necessários para a sua API com os seguintes verbos, GET, POST, PUT e DELETE. conforme o exemplo abaixo.<br>
<br>

![Arquivos Gerados](https://raw.githubusercontent.com/oevertonsouza/advplcodegen/apis/docImg/fontesgerados.png)

<br>
Compile seus fontes e teste sua API usando Postman ou qualquer outro software de requisições HTTP rest.
<br>

Nota:<br>
No metodo GET poderá ser executado como uma busca unica passando o valor da coluna chave escolida no comando addentity no Parametro do Path  e as demais colunas do indice primario nos parametros query.<br>
<br>
Caso tenha alguma duvida sobre a estrutura gerada haverá uma documentação da API em dois arquivos para cada API gerada, no diretório DOC do seu projeto no padrão OpenAPI, um arquivo com a strutura body e um arquivo com a estrutura da API, conforme o comite de API's.<br>
Caso a sua API não esteja funcionando ou com comportamento inadequado, haverá 5 casos de teste do CRUD do seu projeto em ADVPR no diretorio test do seu projeto.
<br>
<br>
 Colabore com esse projeto, caso tenha algum problema no uso ou sugestão comente. 
<br>


