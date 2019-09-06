# Fontes de exemplo

Nesta pasta temos uma API gerada a partir de uma entidade para servir de exemplo e estudo. Com estes exemplos fica mais fácil entender onde implementar as validações, regras de negócios, persistência de dados, etc.
Pretendemos abordar aqui:

 - [x] Estrutura de pastas
 - [ ] Detalhamento das classes criadas
 - [ ] Diagrama de sequência
 
## Estrutura de pastas
O projeto é criado dividindo os fontes por pastas que os agrupam por funcionalidade. Vamos detalhar cada uma delas posteriormente. Abaixo temos a estrutura criada:

 - src_sample
	 - [x] api
	 - [x] collection
	 - [ ] command
	 - [ ] dao
	 - [ ] doc
	 - [ ] entity
	 - [ ] lib
	 - [ ] mapper
	 - [x] request
	 - [ ] test
	 - [ ] validate

## Detalhamento das classes
### Classes "api"
São as classes onde criamos os verbos das APIs (GET, PUT, POST e DELETE), elas são implementações das classes WSRESTFUL do framework ADVPL que está documentada no [TDN](https://tdn.totvs.com/display/framework/WSRESTFUL) 
Buscamos utilizar nestas classes o padrão de projeto estrutural [FACADE](https://sourcemaking.com/design_patterns/facade) e comportamental [TEMPLATE METHOD](https://sourcemaking.com/design_patterns/template_method). Nele apenas definimos "**o caminho a se seguir**", sem necessariamente dizer o "como seguir". O "como" fica de responsabilidade das demais classes implementar.

**Importante:** Dentro da implementação de cada verbo da API, apenas fazemos a chamada dos passos que devem ser seguidos para atender a requisição. **Esta não é uma classe para implementar regras de negócio, validações ou persistência de dados.**

**Exemplo**
[colocar imagem]

### Classes Request
Esta classe é responsável por orquestrar o tratamento da entrada do dado, seu processamento e o tratamento de sua resposta.
Se a classe API diz o caminho, aqui começamos a detalhar o como. Aqui queremos centralizar como o padrão de implementação de APIs da Totvs deve ser implementado.
**Principais métodos:**

 **checkAuth()**
	Chama uma classe responsável por fazer a autenticação da requisição. Podemos, por exemplo, recuperar um token da requisição e passar para um serviço de oAuth2 autenticar.
 **applyFields()**
 Aqui devemos recuperar os fields setados na requisição e prepará-los para serem aplicados no Json de resposta
 **applyPageSize()**
 Aqui devemos recuperar o pagesize setado na requisição e preparar a requisição responder com a página esperada
 **checkBody()**
Aqui é feito o parse do Json que chegou na requisição e verificado se ele está integro.
**getSuccess()**
Devolve se houve sucesso no processamento da requisição.
**initRequest()**
Este é um **hookmethod** ou como conhecido no ADVPL, **um tipo de ponto de entrada**. Este método será sempre chamado no início da requisição, então aqui podemos aplicar regras no início do nosso processo e classes filhas podem sobrescrever esse método para aplicar regras específicas. 

> **Nota:** Este modelo permite uma extensão mais fácil dos comportamentos, sem precisar alterar toda a estrutura do programa. Ele será bastante usado nas demais classes.

**endRequest()**
Outro hookmethod, mas executado ao final da requisição. Aqui recuperamos o status do processamento, o Json de resposta e setamos na requisição.
**serializeFault()**
Método que monta o Json de erro que será adicionado na resposta

**procGet()**
Processa o verbo **GET**. Aqui solicitamos para as classes **Collection** que o registro seja recuperado e depois pedimos à classe **Entity** que serialize o Json com a resposta. 
 > **Nota:** Devemos lembrar que nesse momento o pageSize e Fields já estão setados, então não precisamos nos preocupar seu tratamento. Afinal, não é responsabilidade desse método fazer isso ;)

**procDelete()**
Processa o verbo **DELETE**. Aqui solicitamos para as classes **Collection** se encarreguem de deletar o registro. Se alguma validação for necessária, o ideal seria criar uma classe **Validate** e chamar ela antes de pedir para a **Collection** deletar o registro.
**procPost()**
Processa o verbo **POST**. Neste método, solicitamos que a classe Validate execute as validações para o registro que estamos processando. Estas validações podem ser de estrutura ou de negócio, mas é importante que sejam feitas dentro da classe **Validade**, para não haver confusão de quem faz o que =].
Na classe **Validate** seria possível até instanciar um Model (FWLoadModel) e solicitar que, por meio do oModel:vldData(), que as validações do model fossem executadas.
 > **Nota:** Precisamos nos atentar ao tempo gasto para executar a validação, pois quando falamos de APIs que podem receber centenas de requisições por segundo, cada milisegundo conta. Sempre é valido fazer uma prova de conceito (POC) para comparar os tempos antes de decidir o modelo a se adotar. Principal cuidado ao colocar um Model de MVC junto no processamento de uma requisição.

**Importante:** A responsabilidade para fazer a chamada da persistência dos dados (vulgo commit) é passada para a classe CmdPostClt (classe Command). Essa decisão foi tomada para permitir, de forma genérica, que o comando Commit fosse chamado sem que a classe que está chamando saiba quem a executará. Esse padrão de projeto é conhecido como [Command](https://sourcemaking.com/design_patterns/command). Dessa forma, podemos tanto passar uma Collection para orquestrar o commit, quanto um Model MVC.

**procLotePost()**
Processa o verbo **POST** recebido em lote. Aqui iremos percorrer o array de registros recebidos no lote e realizar seu processamento unitário (procPost). 
> **Nota:** Outro comportamento que este método poderia ter seria adicionar a requisição em uma fila, que seria processada depois, e devolver um token para o solicitante dizendo que em breve o processamento será realizado.

**procPut()**
Processa o verbo **PUT**. Assim como o procPost, é feita a validação do registro e depois solicitada a alteração dos dados.
**Importante:** A responsabilidade para fazer a chamada da persistência dos dados (vulgo commit) é passada para a classe CmdPutClt (classe Command). Essa decisão foi tomada para permitir, de forma genérica, que o comando Commit fosse executado sem que a classe que está chamando saiba quem a executará. Esse padrão de projeto é conhecido como [Command](https://sourcemaking.com/design_patterns/command). Dessa forma, podemos tanto passar uma Collection para orquestrar o commit, quanto um Model MVC.

**buildBody(oEntity)**
Este método irá solicitar a entidade para serializar seus dados e devolver o Json para a requisição

### Classes Collection
Essas classes tem por objetivo fornecer uma listagem de objetos que podem ser manipulados. Para isso é necessário fazer a comunicação entre as classes de processamento (request, command, etc...) e as classes de acesso ao dado (DAOs e Mapper).
Não aconselhamos incluir validações e regras de negócio nessas classes, visto que o objetivo da collection é apenas chamar as classes de acesso a dados e devolver objetos já mapeados com os dados encontrados.
Esta classe aplica de forma explícita o padrão de projetos [Iterator](https://sourcemaking.com/design_patterns/iterator). Este padrão provê uma forma de acessar uma lista de resultados independente de como essa lista foi criada. No nosso caso, estamos criando uma lista de objetos e permitindo que ela seja percorrida chamando apenas os métodos hasNext() e getNext(). Nosso sonho é que todas as listas do ADVPL (Array, HashMap, etc.) sejam assim =]

**Principais métodos:**
**found()** Informa se houve sucesso ao chamar um comando de banco.
**hasNext()** Diz se há mais registros na lista para processar.
**getNext()** Devolve o próximo objeto da lista.
**mapFromJson(cJson)** Cria um objeto mapeado com os dados do Json.
**applyPageSize()** Aplica o tamanho de página esperado para a busca
**applyOrder()** Aplica a ordem do resultado esperado para a busca
**setValue()** Seta um valor na Collection, esse valor poderá ser recuperado em uma busca, ou gravado no banco.
**getValue()** Devolve um valor setado na collection.
**commit()** Chama o DAO para fazer a persistência dos dados.
**insert()** Chama o DAO para fazer a persistência dos dados.
**update()** Chama o DAO para fazer a persistência dos dados.
**delete()** Chama o DAO para fazer a persistência dos dados.
**buscar()** Realiza uma busca no DAO com os dados que foram setados na Collection
**bscChaPrim()** Realiza a busca no DAO pela chave primária da entidade.
