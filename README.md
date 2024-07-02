# Trabalho SD 2024
Este repositório faz parte da entrega do trabalho prático da disciplina de Sistemas Distribuídos da UFSC Araranguá 2024/1

<h1 align="center" style="font-weight: bold;">Trabalho Prático - SD - 2024/1 
<br>Antônio Pedro Cacharosque e Pedro Henrique Gonçalves Ceolin
</h1>

<p align="center">
  <a href="#destino">AcordoDestino</a> • 
  <a href="#bully">Algoritmo Bully</a>
</p>

<h2 id="bully">BullyAlgorithm</h2>

### Sobre

O BullyAlgorithm é um algoritimo que simula o algoritimo de bully, o algoritimo é feito em sistemas multiagents com base em um framework chamado JaCaMo que em suma é uma junção de frameworks o Jason que seria a parte dos agentes que tem como base o ASL (agentspeak language), Cartago uma framework para trabalhar com o Jason, um framework baseado em artefatos, e por fim o Moise um framework para a estruturação dos agentes.

A ideia do codigo é simular o algoritimo de Bully, o sistema inicia com uma interface grafica e o sistema espera que o botão iniciar seja apertado primeiramente. Após o botão de iniciar o sistema o usuario poderá apertar qualquer botão na interface, são eles o botão de matar um processo que espera que você tenha digitado um numero valido de processo no campo de texto, esse botão ira matar o processo escolhido, o proximo botão é o botão de reviver um processo que vai ressucitar um processo previamente morto, e por fim o botão de qual processo vai iniciar a percepção de que o processo líder está morto.

### Como executar localmente

#### Pré requisitos

- Java 17+
- Gradle 8.7+

#### Passo a Passo

Acessar a pasta do projeto SequencerAlgorithmJava

```bash
cd BullyAlgorithm
```

Rodar o comando abaixo na raiz do projeto:

```bash
gradle run
```

Depois disso ele vai pegar todas as dependencias necessarias e vai rodar o programa abrindo a interface grafica.

Qualquer dificuldade em rodar o programa mais informações podem ser adquiridas no link a seguir [Instalação JaCaMo](https://github.com/jacamo-lang/jacamo/blob/main/doc/install.adoc)

<h2 id="visualSequencer">SequencerAlgorithm</h2>

### Sobre
