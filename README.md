# Trabalho SD 2024
Este repositório faz parte da entrega do trabalho prático da disciplina de Sistemas Distribuídos da UFSC Araranguá 2024/1

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
cd AcordoDestino
```

Rodar o comando abaixo na raiz do projeto:

```bash
python3 AcordoDestino.py
```

<h2 id="bully">BullyAlgorithm</h2>

### Sobre

O BullyAlgorithm é um algoritimo que simula o algoritimo de bully, o algoritimo é feito em sistemas multiagents com base em um framework chamado JaCaMo que em suma é uma junção de frameworks o Jason que seria a parte dos agentes que tem como base o ASL (agentspeak language), Cartago uma framework para trabalhar com o Jason, um framework baseado em artefatos, e por fim o Moise um framework para a estruturação dos agentes.

A ideia do codigo é simular o algoritimo de Bully, o sistema inicia com uma interface grafica e o sistema espera que o botão iniciar seja apertado primeiramente. Após o botão de iniciar o sistema o usuario poderá apertar qualquer botão na interface, são eles o botão de matar um processo que espera que você tenha digitado um numero valido de processo no campo de texto, esse botão ira matar o processo escolhido, o proximo botão é o botão de reviver um processo que vai ressucitar um processo previamente morto, e por fim o botão de qual processo vai iniciar a percepção de que o processo líder está morto.

### Como executar localmente

#### Pré requisitos

- Python 3

#### Passo a Passo

Acessar a pasta do projeto SequencerAlgorithmJava

```bash
cd BullyAlgorithm
```

Rodar o comando abaixo na raiz do projeto:

```bash
python3 
```
