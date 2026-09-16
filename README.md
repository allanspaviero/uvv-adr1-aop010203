# Preços de Combustíveis — Vila Velha/ES

Projeto de extensão da disciplina **Arquitetura de Dados Relacionais I** — Universidade Vila Velha (UVV).

Banco de dados relacional que armazena e disponibiliza informações sobre o preço dos combustíveis da região, com os resultados divulgados para a comunidade.

**Allan Spaviero Alpoim** — matrícula 202636574

---

## Etapas

| Etapa | Entrega | Situação |
|---|---|---|
| **AOP01** | Projeto conceitual — modelo ER completo | entregue |
| **AOP02** | Projeto lógico (modelo relacional em 3FN) e projeto físico em MySQL | [`aop02/`](aop02/) |
| **AOP03** | Divulgação dos resultados para a comunidade | [`aop03/`](aop03/) |

## AOP03 — o site público

**<https://allanspaviero.github.io/uvv-adr1-aop010203/>**

Website que permite a qualquer pessoa efetuar as quatro consultas exigidas pelo
enunciado, com os dois gráficos de evolução do preço médio e as planilhas para
download.

O site não reimplementa as consultas: ele abre o banco de dados dentro do próprio
navegador, com SQLite compilado para WebAssembly, e executa os mesmos arquivos
`.sql` da AOP02 sem alterar uma linha. Cada seção mostra, atrás de um botão, o
comando exato que produziu a tabela acima dela.

Detalhes em [`aop03/README.md`](aop03/README.md).

## AOP02 — o que já existe

Modelo relacional na 3ª Forma Normal implementado em **MySQL 8.0**, com cinco tabelas, dados reais e as consultas exigidas pelo enunciado.

```
aop02/sql/        DDL, carga de dados e as consultas obrigatórias
aop02/scripts/    coleta dos dados na ANP, geração dos artefatos e verificação
aop02/docs/       diagrama do modelo relacional e roteiro de montagem da entrega
```

Comece por [`aop02/README.md`](aop02/README.md), que explica a conversão do modelo conceitual e como executar tudo.

### O modelo

Cinco tabelas, com os atributos especiais do modelo conceitual tratados assim:

| Construto no modelo ER | Solução no relacional |
|---|---|
| `Telefone` (multivalorado) | tabela `telefone_posto` — 1FN |
| `Endereço` (composto) | colunas `rua`, `numero`, `cep` em `posto` |
| `Bairro` (parte do composto) | tabela `bairro` com chave estrangeira — 3FN |
| `Qtd_Amostras` (derivado) | view `vw_posto_amostras`, não armazenada |

### Os dados

**Série Histórica de Preços de Combustíveis da ANP**, município de Vila Velha/ES, de janeiro a agosto de 2026: 5 postos em 3 bairros, 569 coletas de preço cobrindo gasolina, gasolina aditivada, etanol e diesel, com 27 a 31 datas distintas por posto.

Os CSVs originais não são versionados por causa do tamanho (~93 MB). Para reproduzir a carga do zero:

```bash
cd aop02
python scripts/baixar_anp.py && python scripts/gerar_dados.py
```

Fonte: [Série Histórica de Preços de Combustíveis — ANP](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/serie-historica-de-precos-de-combustiveis)

## Executando o banco

```bash
mysql -u root -p < aop02/sql/01-schema.sql
mysql -u root -p < aop02/sql/02-dados.sql
```

Para conferir o schema, os dados e as consultas sem precisar de um servidor MySQL instalado:

```bash
python aop02/scripts/validar.py
```

## Licença

Trabalho acadêmico, disponibilizado publicamente para fins de estudo e para a divulgação à comunidade prevista na AOP03.
