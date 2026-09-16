# Texto do relatório da AOP03 — para revisão

Este arquivo é o rascunho do conteúdo do PDF de entrega. **Revise o texto aqui**;
quando estiver aprovado, ele vira o PDF por script, do mesmo jeito que a AOP02.

Os campos entre `[colchetes]` são fatos que só existem depois da videoconferência.
Preencha-os aqui mesmo, ou me passe os valores que eu preencho.

---

## Capa

```
                    UNIVERSIDADE VILA VELHA
           ARQUITETURA DE DADOS RELACIONAIS I

                 ALLAN SPAVIERO ALPOIM
                    Matrícula 202636574


         PROJETO DE EXTENSÃO — PREÇOS DE COMBUSTÍVEIS
                    AOP03: DIVULGAÇÃO DO
                 TRABALHO PARA A COMUNIDADE


                    Vila Velha / ES
                          2026
```

---

## 1. O projeto

O Projeto de Extensão desta disciplina pediu um banco de dados relacional capaz
de armazenar e fornecer informações sobre o preço dos combustíveis da região. As
duas primeiras etapas construíram esse banco: a AOP01 entregou o projeto
conceitual em modelo ER e a AOP02 o converteu em um modelo relacional na 3ª Forma
Normal, implementado em MySQL 8.0 e carregado com 569 coletas de preço da Série
Histórica da ANP, cobrindo cinco postos de três bairros de Vila Velha entre 7 de
janeiro e 26 de agosto de 2026.

Esta terceira etapa trata do que fazer com esse banco: devolver a informação a
quem ela interessa. Das três formas de divulgação previstas no enunciado, foi
escolhida a **criação de um website** (opção *a*), publicado em endereço público
e gratuito:

**https://allanspaviero.github.io/uvv-adr1-aop010203/**

A escolha não foi apenas de conveniência. Preço de combustível é uma informação
que perde o valor quando fica parada: quem abastece precisa consultá-la no
momento em que decide onde parar. Um site aberto, sem cadastro e que funciona no
celular chega a essa pessoa de um jeito que um relatório impresso não chega.

## 2. O que o site faz

O site permite ao usuário efetuar as quatro consultas exigidas pelo item II.d do
enunciado e disponibiliza as planilhas e os gráficos do item II.e. Cada consulta
ocupa uma aba, e o menu do topo troca a aba sem recarregar a página.

| Aba do site | Requisito atendido |
|---|---|
| Mais barato | resposta direta ao usuário comum, a partir da consulta I |
| Menor e maior preço | II.d.I — menor e maior preço de cada combustível |
| Média e amostras | II.d.II — preço médio e quantidade de amostras por posto |
| Preço mais recente | II.d.III — última cotação de cada posto |
| Evolução no tempo | II.d.IV — série de um combustível em um posto, com seletores |
| Gráficos | II.e.I e II.e.II — evolução do preço médio, no total e por posto |
| Planilhas | II.e — planilha com uma aba por consulta, mais os arquivos CSV |

Há um ponto do site que merece registro por ser o que o liga ao trabalho das
etapas anteriores: **as tabelas não são um resumo pré-calculado**. O navegador
abre o banco de dados e executa os mesmos arquivos `.sql` entregues no projeto
físico da AOP02, sem alterar uma linha. Por isso cada aba tem um botão "ver a
consulta SQL" que mostra exatamente o comando que produziu a tabela exibida
acima dele. Na consulta IV, o posto e o combustível escolhidos pelo usuário
substituem os dois valores do `WHERE`, e o SQL exibido acompanha a substituição.

O site não depende de servidor nem de banco de dados hospedado: o SQLite roda
dentro do próprio navegador, compilado para WebAssembly. Isso mantém a
divulgação no ar sem custo e sem risco de sair do ar por falta de manutenção —
o que importa quando o objetivo é que a comunidade continue usando depois da
entrega.

## 3. A ação de divulgação

A divulgação foi feita em **[data]**, por videoconferência, na plataforma
**[Teams / Google Meet / Discord]**, com **[número]** participantes, moradores de
Vila Velha que abastecem na região.

A sessão teve três momentos. No primeiro, os participantes foram informados de
que a conversa seria registrada em imagens destinadas exclusivamente à entrega
desta disciplina, e todos confirmaram concordância antes de qualquer captura. No
segundo, o site foi apresentado com a tela compartilhada, percorrendo cada uma
das consultas. No terceiro — o mais importante para o objetivo da atividade — o
endereço foi enviado no chat e os próprios participantes passaram a navegar, em
seus computadores e celulares, respondendo a perguntas que exigiam consultar o
site: qual posto estava com a gasolina mais barata, em que bairro ficava, qual
foi o etanol mais barato do período e se o diesel subiu ou caiu entre janeiro e
agosto.

Essa inversão foi proposital. Uma apresentação em que o autor fala e os demais
assistem demonstra divulgação, mas não demonstra uso. As perguntas obrigaram os
participantes a encontrar a informação sozinhos, e foi isso que as evidências
registraram.

## 4. Evidências

*(cada imagem entra aqui com a legenda abaixo)*

**Figura 1 — Ambiente da sessão.** Início da videoconferência, com os
participantes já conectados, antes da apresentação. **[data, horário]**

**Figura 2 — Apresentação do site.** Tela compartilhada exibindo uma das
consultas do banco de dados, com a janela da chamada visível.
**[data, horário]**

**Figura 3 — Uso pela comunidade.** Tela de um participante navegando no site
por conta própria para responder a uma das perguntas. **[data, horário]**

**Figura 4 — Interação no chat.** Envio do endereço e respostas dos
participantes às perguntas feitas durante a sessão. **[data, horário]**

**Figura 5 — Planilhas disponíveis.** Aba de download dos dados, mostrada aos
participantes ao final da sessão. **[data, horário]**

## 5. Resultado

O site permanece no ar e acessível a qualquer pessoa, sem cadastro e sem custo.
Os **[número]** participantes da sessão conseguiram encontrar, sozinhos, as
informações solicitadas, o que indica que a interface cumpre o objetivo de
entregar o conteúdo do banco de dados a um usuário comum — alguém que não
conhece o modelo relacional por trás e não precisa conhecer.

Além da consulta pelo site, os dados ficam disponíveis para download em planilha
e em arquivos CSV, de modo que quem quiser trabalhar os números por conta
própria possa fazê-lo. O código-fonte e os scripts do banco estão publicados em
<https://github.com/allanspaviero/uvv-adr1-aop010203>.

---

## Notas para você, que não entram no PDF

- **Preencher antes de gerar:** data, plataforma, número de participantes e o
  horário de cada figura. São seis campos.
- **Se a sessão render mais ou menos de cinco prints**, me avise: o texto da
  seção 4 se ajusta ao número real de figuras.
- **Se algum participante recusar** aparecer em alguma captura, aquela imagem
  não entra — e o texto da seção 3 não precisa mudar.
- A seção sobre cumprimento das regras éticas ficou de fora, como você pediu. O
  consentimento continua sendo pedido na abertura da chamada, conforme o roteiro.
