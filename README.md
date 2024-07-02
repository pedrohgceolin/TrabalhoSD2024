<h1 align="center" style="font-weight: bold;">Trabalho Prático - SD - 2024/1 
<br>Antônio Pedro Cacharosque e Pedro Henrique Gonçalves Ceolin
</h1>

<p align="center">
  <a href="#destino">Acordo no Destino</a> • 
  <a href="#bully">Algoritmo Bully</a>
</p>

<h2 id="destino">Acordo no Destino</h2>

### Sobre

O algoritmo de acordo no destino é um método utilizado em sistemas distribuídos para garantir que todos os nós participantes cheguem a um consenso sobre um valor ou estado comum, mesmo na presença de falhas.

O objetivo principal é cumprir três condições: terminação (todos os nós eventualmente tomam uma decisão), acordo (todos os nós escolhem o mesmo valor) e validade (se todos os nós iniciam com o mesmo valor, esse será valor decidido). 

O processo envolve a proposição de valores, troca de mensagens entre os nós e a decisão final baseada nas informações recebidas.

### Como executar localmente

#### Pré requisitos

- Python 3

#### Passo a Passo

Acessar a pasta do projeto AcordoDestino

```bash
cd acordoDestino
```

Rodar o comando abaixo na raiz do projeto:

```bash
python acordoDestino.py
```

<h2 id="bully">BullyAlgorithm</h2>

### Sobre

O algoritmo de eleição Bully é um método utilizado para selecionar um coordenador ou líder entre os nós. Quando um nó detecta que o coordenador atual falhou, ele inicia o processo de eleição. O nó que inicia a eleição envia uma mensagem a todos os nós com IDs maiores que o seu, solicitando uma eleição.

Os nós que recebem a solicitação de eleição respondem e também iniciam suas próprias eleições, enviando mensagens para todos os nós com IDs maiores que os seus. Isso continua até que um nó não receba resposta de nenhum nó com ID maior, declarando-se o novo coordenador. O novo coordenador então anuncia sua vitória para todos os nós da rede, assumindo a função de líder até que uma nova falha seja detectada. Esse algoritmo é chamado de "bully" porque o nó com o maior ID acaba "intimidando" os outros e se tornando o líder.

### Como executar localmente

#### Pré requisitos

- Python 3

#### Passo a Passo

Acessar a pasta do projeto SequencerAlgorithmJava

```bash
cd algBully
```
Rodar o comando abaixo na raiz do projeto:

```bash
python3 algBully.py
```
