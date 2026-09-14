# Roteiro do PDF de entrega — AOP02

**Allan Spaviero Alpoim — 202636574**

O item III.d exige um PDF único reunindo os prints do Projeto Lógico e do Projeto Físico, com contextualização, **e o nome do integrante visível nos prints**. Todos os scripts deste repositório já trazem o nome e a matrícula no cabeçalho de comentário — então basta que o editor SQL do Workbench esteja mostrando o topo do arquivo em cada captura, e o requisito do nome está cumprido automaticamente.

São **13 prints**.

> O banco `precos_combustiveis` **já está criado e povoado** no seu MySQL 8.0.46: 3 bairros, 5 postos, 7 telefones, 4 combustíveis e 569 coletas. As 4 consultas já foram executadas e retornam 8, 20, 20 e 31 linhas. Você não precisa rodar `01-schema.sql` nem `02-dados.sql` de novo — só vai abri-los no Workbench para printar. Se algum print der erro, é configuração da conexão, não do script.

---

# Passo 0 — Primeiros passos no MySQL Workbench

*Leia esta parte se você nunca usou o Workbench. Se já estiver à vontade com ele, pule para a Capa.*

## 0.1 Abrir e conectar

Abra o **MySQL Workbench** pelo menu Iniciar. Na tela inicial existe um retângulo escrito **`Local instance MySQL80`** — é a sua conexão com o servidor, que já está rodando. Dê um clique nele.

Vai aparecer uma caixa pedindo a senha do usuário `root`. Digite **`teste1`**, marque **`Save password in vault`** (assim ele não pergunta de novo) e confirme.

> Se o retângulo não existir, clique no **`+`** ao lado de "MySQL Connections" e preencha: Connection Name `Local`, Hostname `127.0.0.1`, Port `3306`, Username `root`. Depois clique nele e informe a senha.

## 0.2 Entender a tela

Depois de conectar, a janela tem quatro áreas. Vale reconhecê-las antes de continuar, porque o roteiro se refere a elas o tempo todo:

| Área | Onde fica | Para que serve |
|---|---|---|
| **Navigator / Schemas** | coluna da esquerda | lista os bancos. Expanda `precos_combustiveis` → `Tables` para ver as 5 tabelas |
| **Editor de SQL** | centro, área branca grande | onde você digita ou abre os scripts |
| **Result Grid** | abaixo do editor | a tabela de resultados de cada consulta |
| **Action Output** | rodapé | o log: linha verde = deu certo, vermelha = erro |

Se a lista de schemas estiver vazia, clique no ícone de **atualizar** (duas setas em círculo) no cabeçalho do painel Schemas.

## 0.3 Abrir um script

`File > Open SQL Script...` (ou `Ctrl+Shift+O`), navegue até a pasta do projeto e escolha o arquivo. Ele abre numa aba nova do editor.

Os três arquivos ficam em:
`C:\Users\allan\Documents\repositorio-local\uvv-adr1-aop02\sql\`

## 0.4 Executar — a diferença que importa

Existem **dois** botões de raio na barra de ferramentas, e confundi-los é o erro nº 1 de quem está começando:

| Botão | Atalho | O que faz |
|---|---|---|
| ⚡ raio **sozinho** | `Ctrl+Shift+Enter` | executa **o script inteiro** |
| ⚡ raio com **cursor** ao lado | `Ctrl+Enter` | executa **só o comando onde está o cursor** |

Para o roteiro você vai usar quase sempre o **segundo** (`Ctrl+Enter`): clique dentro da consulta que quer rodar e aperte. Assim o Result Grid mostra **um** resultado por vez, que é o que você precisa printar. Se rodar o script todo, o Workbench abre várias abas de resultado empilhadas e o print fica confuso.

## 0.5 Ver quantas linhas voltaram

No canto inferior direito do Result Grid o Workbench escreve algo como `20 row(s) returned`. Esse texto é importante em alguns prints — sempre enquadre ele na captura.

## 0.6 Tirar o print

No Windows, **`Win + Shift + S`** abre a ferramenta de captura. Arraste selecionando a área desejada; a imagem vai para a área de transferência e você cola direto no Word com `Ctrl+V`.

Capture a **janela do Workbench**, não a tela inteira — o professor precisa enxergar o texto.

## 0.7 A regra do nome nos prints

O item III.d exige seu nome nos prints. Todos os scripts começam com um comentário assim:

```sql
-- AOP02 - Arquitetura de Dados Relacionais I - UVV
-- Allan Spaviero Alpoim - matricula 202636574
```

Então **antes de cada captura, role o editor até o topo do arquivo** para que esse cabeçalho apareça. Isso resolve o requisito sem você ter que escrever seu nome em lugar nenhum.

Nos prints que são só de resultado (sem script à vista), deixe a aba do arquivo visível ou digite seu nome como comentário acima da consulta.

---

## Capa

> **AOP02 — Projeto Lógico e Físico**
> Arquitetura de Dados Relacionais I — UVV
> Projeto de Extensão: Preços de Combustíveis — Vila Velha/ES
> Allan Spaviero Alpoim — matrícula 202636574
> Prof. Jean-Rémi Bourguet — setembro de 2026

---

## Seção 1 — Correção acatada da AOP01

Texto sugerido:

> Na correção da AOP01 foi apontada uma inversão na notação das cardinalidades do diagrama ER. O diagrama abaixo apresenta a versão corrigida, que serviu de base para a conversão ao modelo relacional. A leitura semântica do modelo permanece a mesma — um posto registra várias coletas e cada coleta pertence a exatamente um posto e a exatamente um combustível —, de modo que o projeto lógico e físico desta etapa reflete o modelo já corrigido.

**Print 1** — `docs/diagramaer-aop01-corrigido.drawio` aberto no draw.io, mostrando o ER inteiro com as cardinalidades trocadas.

Se quiser deixar o contraste explícito, coloque lado a lado o `diagramaer-aop01.jpg` original (antes) e o corrigido (depois).

---

## Seção 2 — Projeto Lógico

Texto sugerido:

> O modelo conceitual foi convertido para o modelo relacional em 3ª Forma Normal. O atributo multivalorado `Telefone` deu origem à tabela `telefone_posto`, atendendo à 1FN. O atributo composto `Endereço` foi decomposto nas colunas `rua`, `numero` e `cep`, e sua parcela `Bairro` foi promovida a tabela própria, de modo que `cidade` e `uf` não fiquem dependentes de forma transitiva do posto — exigência da 3FN. O atributo derivado `Qtd_Amostras` não foi armazenado: é calculado pela view `vw_posto_amostras`. Os dois relacionamentos 1:N do modelo conceitual, `Registra` e `Referente_Cbstvl`, tornaram-se chaves estrangeiras obrigatórias na tabela `coleta`.

**Print 2** — O diagrama EER gerado pelo MySQL Workbench.

Este é o print mais importante da entrega: é ele que cumpre a exigência de "diagrama feito com uma ferramenta de modelagem". O Workbench monta o diagrama sozinho a partir do banco que já está criado — você não desenha nada.

**Como obter, tela por tela:**

1. No menu de cima, clique em **`Database` > `Reverse Engineer...`** (atalho `Ctrl+R`). Abre um assistente de 6 telas.
2. **Connection Options** — a conexão `Local instance MySQL80` já vem selecionada. Clique **`Next`**. Se pedir a senha, é `teste1`.
3. **Connect to DBMS** — ele conecta e lista tarefas com ✔ verde. Clique **`Next`**.
4. **Select Schemas** — aqui você precisa agir: **marque a caixinha do `precos_combustiveis`**. Se deixar desmarcado, o diagrama sai vazio. Clique **`Next`**.
5. **Retrieve Objects** — mais ✔ verdes. Clique **`Next`**.
6. **Select Objects** — deixe como está (todas as tabelas vêm marcadas). Clique **`Execute`**.
7. **Results** — clique **`Close`**.

O diagrama abre sozinho numa aba nova, com as 5 tabelas e as linhas de relacionamento ligando as chaves estrangeiras.

**Antes de printar, organize:** as tabelas nascem empilhadas de qualquer jeito. Arraste cada uma pelo seu título até que nenhuma linha de relacionamento cruze outra. Uma disposição que funciona bem:

```
   bairro  ────  posto  ────  coleta  ────  combustivel
                   │
            telefone_posto
```

Se ficarem grandes demais para caber na tela, use `Ctrl+-` para reduzir o zoom, ou o seletor de porcentagem na barra da aba do diagrama. Só então capture.

> **Plano B** — se o assistente falhar por algum motivo de conexão, abra `docs/modelo-logico.drawio` no site <https://app.diagrams.net> (`File > Open from > Device`) e printe esse. Ele tem o mesmo conteúdo: as 5 tabelas com colunas, tipos, PK, FK e UNIQUE.

**Print 3** — A aba de dicionário: dê duplo clique em `coleta` no EER e capture a lista de colunas com tipos, e a aba `Foreign Keys`. Serve para evidenciar datatypes e chaves, que o enunciado pede nominalmente.

---

## Seção 3 — Projeto Físico: DDL

Texto sugerido:

> A implementação física foi feita em MySQL 8.0 com o mecanismo InnoDB. O script de criação emprega os tipos de restrição trabalhados na disciplina: chave primária, chave estrangeira com ações referenciais, chave única, obrigatoriedade, verificação de domínio e valor padrão.

**Print 4** — `sql/01-schema.sql` aberto no Workbench, **rolado até o topo**, mostrando o cabeçalho com seu nome e matrícula e o início do DDL.

**Print 5** — A parte do script com as tabelas `posto` e `coleta` visíveis, onde aparecem `PRIMARY KEY`, `FOREIGN KEY ... ON UPDATE CASCADE ON DELETE RESTRICT`, `UNIQUE` e `CHECK`.

**Print 6** — O painel `Action Output` com todas as linhas verdes, provando que o script roda sem erro.

Para conseguir este print você precisa **executar os scripts de novo**. Isso é seguro, mas exige atenção à ordem:

> ⚠️ O `01-schema.sql` começa com `DROP DATABASE IF EXISTS precos_combustiveis`. Ele **apaga e recria o banco do zero**, o que deixa as tabelas vazias. Se você rodá-lo, **precisa rodar o `02-dados.sql` logo em seguida**, senão os prints da Seção 4 sairão sem dados.

Sequência correta:

1. abra `01-schema.sql`, execute o script inteiro (`Ctrl+Shift+Enter`)
2. abra `02-dados.sql`, execute o script inteiro (`Ctrl+Shift+Enter`) — demora alguns segundos, são 569 inserções
3. capture o `Action Output` mostrando as linhas verdes das duas execuções

Se preferir não mexer no banco já pronto, pule este print: o Print 7 e o Print 8, mostrando as tabelas povoadas, já provam que os scripts funcionaram.

---

## Seção 4 — Projeto Físico: tabelas povoadas

Texto sugerido:

> Os dados provêm da Série Histórica de Preços de Combustíveis da ANP, referentes ao município de Vila Velha/ES entre janeiro e agosto de 2026. Foram selecionados 5 postos distribuídos por 3 bairros, com 569 coletas de preço cobrindo os quatro combustíveis exigidos, sendo de 27 a 31 datas distintas por posto.

Abra **`sql/04-tabelas-povoadas.sql`** (`Ctrl+Shift+O`). Ele já tem todas as consultas desta seção, na ordem, com seu nome no cabeçalho.

Aqui, diferente da Seção 5, o arquivo tem **várias** consultas — então rode **uma de cada vez**: clique dentro da consulta desejada e aperte **`Ctrl+Enter`**. Se rodar o arquivo inteiro, os resultados se empilham em abas e o print fica ilegível.

**Print 7 — o resumo.** Rode o bloco **A** (o `SELECT ... UNION ALL` com as contagens). Ele devolve as 5 tabelas com a quantidade de linhas de cada uma:

| tabela | qtd_linhas |
|---|---|
| bairro | 3 |
| posto | 5 |
| telefone_posto | 7 |
| combustivel | 4 |
| coleta | 569 |

Este é o print que responde diretamente ao "todas as tabelas povoadas" do enunciado: uma imagem só provando que nenhuma tabela do modelo ficou vazia.

**Print 8 — o conteúdo das tabelas menores.** Rode os blocos **B.1** a **B.4** (`bairro`, `combustivel`, `posto`, `telefone_posto`) e capture. São tabelas curtas, então dá para agrupar duas ou três por captura.

Ao printar `telefone_posto`, vale a contextualização: *"A tabela `telefone_posto` materializa o atributo multivalorado `Telefone` do modelo conceitual — note que os postos 1 e 2 possuem dois números cada, o que seria impossível representar numa única coluna."*

**Print 9 — a tabela `coleta`.** Rode o bloco **B.5**. Capture mostrando o rodapé do Result Grid, onde o Workbench informa `569 row(s) returned`.

Logo abaixo, no bloco **C**, há a mesma tabela com os nomes resolvidos no lugar dos IDs. Se couber um print a mais, ele comunica muito melhor ao leitor do PDF do que a tabela crua de chaves estrangeiras.

Rode também o bloco **D** — `SELECT * FROM vw_posto_amostras` — e contextualize: *"O atributo derivado `Qtd_Amostras` do modelo conceitual não é uma coluna armazenada; ele é obtido por esta view, que conta as coletas de cada posto."*

> O bloco **E** do arquivo é opcional e costuma impressionar: ele lista lado a lado cada mínimo exigido pelo enunciado (5 postos, 4 combustíveis, ≥ 2 bairros, ≥ 5 datas por posto) e o valor efetivamente obtido no banco. Um print dele fecha a seção provando a conformidade item a item.

---

## Seção 5 — Projeto Físico: as consultas do item II.d

Cada consulta obrigatória está no seu **próprio arquivo**, justamente para o print sair limpo. O procedimento é o mesmo para as quatro:

1. `File > Open SQL Script` (`Ctrl+Shift+O`) e escolha o arquivo
2. execute o script inteiro com **`Ctrl+Shift+Enter`** — como só há uma consulta no arquivo, sai um único Result Grid
3. capture com o editor **rolado até o topo**, para o cabeçalho com seu nome aparecer junto do código e do resultado

Assim cada print já contém as três coisas que o professor pede de uma vez: seu nome, o código da consulta e o resultado.

**Print 10** — `sql/03-consulta-1-menor-maior-preco.sql` → **8 linhas**.
Contextualize: *"Menor e maior preço de cada tipo de combustível, com nome do posto, endereço, bairro, tipo, valor e data da coleta. As funções de janela `ROW_NUMBER()` classificam as coletas de cada combustível simultaneamente por valor crescente e decrescente; a primeira posição de cada ordenação é, respectivamente, o menor e o maior preço. São 8 linhas — o par mínimo/máximo de cada um dos 4 combustíveis."*

**Print 11** — `sql/03-consulta-2-media-e-amostras.sql` → **20 linhas**.
Contextualize: *"Para cada posto e cada combustível, a quantidade de amostras coletadas e o preço médio. São 20 linhas, uma para cada combinação dos 5 postos com os 4 combustíveis."*

**Print 12** — `sql/03-consulta-3-preco-mais-recente.sql` → **20 linhas**.
Contextualize: *"Para cada posto e cada combustível, apenas a cotação mais recente. A função de janela particiona as coletas por posto e combustível e ordena da data mais nova para a mais antiga, tomando somente a primeira."*

**Print 13** — `sql/03-consulta-4-evolucao-preco.sql` → **31 linhas**.
Contextualize: *"Evolução do preço da Gasolina no posto Auto Posto R M ao longo do tempo, ordenada pela data da coleta — 31 registros entre janeiro e agosto de 2026. Alterando os dois valores da cláusula `WHERE` obtém-se a série de qualquer outro posto e combustível."*

> Se o número de linhas no seu Result Grid não bater com o indicado acima, o banco está vazio: rode o `sql/02-dados.sql` e repita.

---

## Seção 6 (opcional, mas recomendada) — Integridade

Um print a mais que costuma valer nota em disciplina de banco: mostre que as restrições **funcionam**, não só que existem.

```sql
-- deve ser recusado pelo CHECK
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (1, 1, '2026-09-01', -1);

-- deve ser recusado pela UNIQUE
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (1, 1, '2026-01-07', 6.19);

-- deve ser recusado pela FOREIGN KEY
INSERT INTO coleta (id_posto, id_combustivel, data_coleta, valor)
VALUES (999, 1, '2026-09-01', 6.19);
```

Capture o `Action Output` com as três mensagens de erro e escreva: *"As restrições declaradas no DDL são efetivamente aplicadas pelo SGBD, rejeitando valor negativo, amostra duplicada para o mesmo posto/combustível/data e referência a posto inexistente."*

---

## Fechamento

Exporte tudo em PDF com as seções na ordem acima. Confira antes de enviar:

- [ ] seu nome aparece legível em pelo menos um print de cada seção
- [ ] o diagrama do modelo relacional está presente e legível
- [ ] as 5 tabelas aparecem povoadas
- [ ] as 4 consultas aparecem com **código e resultado**
- [ ] a fonte dos dados (ANP) está citada no texto

Se preferir, me mande os prints por aqui que eu monto o PDF com toda a contextualização já escrita.
