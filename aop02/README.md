# AOP02 — Projeto Lógico e Físico

**Arquitetura de Dados Relacionais I — UVV**
Allan Spaviero Alpoim — matrícula 202636574
Projeto de Extensão: *Preços de Combustíveis* — Vila Velha/ES

Conversão do projeto conceitual da AOP01 (modelo ER) em modelo relacional na 3ª Forma Normal e sua implementação física em **MySQL 8.0**.

---

## O que tem aqui

```
sql/01-schema.sql      DDL — banco, 5 tabelas, restrições e a view do atributo derivado
sql/02-dados.sql       DML — carga com dados reais da ANP (gerado, não editar à mão)
sql/03-consulta-1-menor-maior-preco.sql    consulta I   (item II.d.I)
sql/03-consulta-2-media-e-amostras.sql     consulta II  (item II.d.II)
sql/03-consulta-3-preco-mais-recente.sql   consulta III (item II.d.III)
sql/03-consulta-4-evolucao-preco.sql       consulta IV  (item II.d.IV)
sql/04-tabelas-povoadas.sql                comprova as 5 tabelas povoadas (item III.d)

scripts/baixar_anp.py    baixa os CSVs mensais da Série Histórica da ANP
scripts/gerar_dados.py   filtra Vila Velha/ES, escolhe os postos e gera 02-dados.sql
scripts/gerar_diagrama.py gera o diagrama lógico em draw.io (plano B do Workbench)
scripts/validar.py       auto-verificação sem precisar de servidor MySQL

docs/ROTEIRO-PDF.md                  o que printar e em que ordem, para montar o PDF
docs/modelo-logico.drawio            diagrama do modelo relacional (plano B)
docs/diagramaer-aop01-corrigido.drawio  ER da AOP01 com a cardinalidade corrigida

dados/                 CSVs brutos da ANP (regeráveis, não versionar)
```

## Como rodar

**1. Criar e povoar o banco** — no MySQL Workbench, abrir e executar nesta ordem:

```
sql/01-schema.sql     →  cria o banco precos_combustiveis e as tabelas
sql/02-dados.sql      →  insere 3 bairros, 5 postos, 4 combustíveis, 569 coletas
sql/03-consulta-*.sql →  uma consulta obrigatória por arquivo, um print cada
sql/04-tabelas-povoadas.sql → comprova que todas as tabelas estão povoadas
```

Ou pela linha de comando. O instalador do MySQL no Windows **não coloca o `mysql.exe` no PATH**, então use o caminho completo:

```bash
"/c/Program Files/MySQL/MySQL Server 8.0/bin/mysql.exe" -u root -p < sql/01-schema.sql
```

> Verificado em **MySQL 8.0.46** (Windows): schema, carga e as 4 consultas executam sem erro, e as restrições `CHECK`, `UNIQUE` e `FOREIGN KEY` rejeitam dado inválido como esperado.

**2. Gerar o diagrama do modelo relacional** no Workbench:
`Database > Reverse Engineer` → conexão local → marcar o schema `precos_combustiveis` → `Next` até `Execute`. O EER sai pronto com tabelas, colunas, chaves e relacionamentos.

**3. Regenerar os dados** (opcional — o `02-dados.sql` já vem pronto):

```bash
python scripts/baixar_anp.py && python scripts/gerar_dados.py
```

**4. Conferir tudo sem MySQL instalado:**

```bash
python scripts/validar.py
```

## Do modelo conceitual (AOP01) ao lógico (AOP02)

| Construto no ER | Vira o quê no relacional | Por quê |
|---|---|---|
| `Telefone` multivalorado | tabela `telefone_posto` | a 1FN proíbe vários valores numa coluna |
| `Endereço` composto | colunas `rua`, `numero`, `cep` em `posto` | atributo composto se decompõe em colunas simples |
| `Bairro` (dentro de Endereço) | tabela `bairro` + FK em `posto` | evita que `cidade`/`uf` fiquem dependentes de forma transitiva do posto (3FN) |
| `Qtd_Amostras` derivado | view `vw_posto_amostras` | atributo derivado não se armazena — calcula-se |
| `Registra` 1:N | FK `coleta.id_posto` NOT NULL | o lado (1,1) vira chave estrangeira obrigatória |
| `Referente_Cbstvl` 1:N | FK `coleta.id_combustivel` NOT NULL | idem |

Restrições usadas: `PRIMARY KEY`, `FOREIGN KEY` (com `ON UPDATE CASCADE` / `ON DELETE RESTRICT`), `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`, `AUTO_INCREMENT`.

## Origem dos dados

**Série Histórica de Preços de Combustíveis — ANP**, meses de janeiro a agosto de 2026, filtrada para o município de Vila Velha/ES. Os arquivos originais trazem, por coleta: revenda, CNPJ, rua, número, bairro, CEP, município, bandeira, produto, data da coleta e valor de venda.

Fonte: <https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis>

O `DIESEL S10` da ANP é o que representa o **Diesel** do requisito II.a — é o diesel efetivamente vendido na bomba e o de maior cobertura na série.

Os telefones em `telefone_posto` **não vêm da ANP** (a série não publica telefone) e são ilustrativos: existem apenas para demonstrar o mapeamento do atributo multivalorado do projeto conceitual. Isso está declarado em comentário dentro do próprio `02-dados.sql`.

## Requisitos do enunciado e onde estão atendidos

| Requisito | Onde |
|---|---|
| II.a — 5 postos, 4 combustíveis | `02-dados.sql`, tabelas `posto` e `combustivel` |
| II.b — ≥ 5 coletas por posto, em datas diferentes | `coleta` — de 27 a 31 datas distintas por posto |
| II.c — ≥ 2 bairros | 3 bairros: Praia de Itaparica, Divino Espirito Santo, Itaparica |
| II.d.I a II.d.IV — as 4 consultas | um arquivo por consulta: `03-consulta-1` a `03-consulta-4` |
| III.d — tabelas povoadas | `04-tabelas-povoadas.sql` |
| III.d — prints com o nome do integrante | cabeçalho de comentário no topo de todo script |

Os itens **II.e** (planilhas e gráficos) e a divulgação à comunidade são da **AOP03**.
